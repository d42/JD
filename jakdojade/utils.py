from functools import reduce
import six
import sys

import editdistance
from six.moves.urllib_parse import urlencode, urlparse, urlunparse


class PassthroughMixin:
    # https://github.com/tomchristie/django-rest-framework/issues/2108 :^)

    def __getattribute__(self, attr):
        try:
            return super(PassthroughMixin, self).__getattribute__(attr)
        except AttributeError:
            info = sys.exc_info()
            try:
                return getattr(self.data, attr)
            except AttributeError:
                six.reraise(info[0], info[1], info[2].tb_next)


class DeferredType:
    def __init__(self, _req, _args, **kwargs):
        self.__data = None
        self.req = self.__deferred_req(_req, _args)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def __deferred_req(query, args):
        def func():
            return query(*args)
        return func

    def __getattr__(self, attr):
        if self.__data is None:
            self.__data = self.req()
        return getattr(self.__data, attr)


def resolve_class(class_name, module_globals):
    if not isinstance(class_name, str):
        return class_name
    elif class_name in module_globals:
        return module_globals[class_name]


def dotted_lowercase_get(dictionary, path):
    def getitem_lowercase(dictionary, key):
        dictionary = {k.lower(): v for k, v in dictionary.items()}
        key = key.lower()
        return dictionary[key]

    return reduce(getitem_lowercase, (path.split('.')), dictionary)


def extract_attribute(objects, attribute=None):
    for o in objects:
        value = getattr(o, attribute if attribute else o._search_attribute)
        yield o, value.lower()


def fuzzy_search(objects, value, attribute=None):
    value = value.lower()

    def score(object_attr):
        _, attr = object_attr
        return editdistance.eval(attr, value) - (5 if value in attr else 0)

    return min(extract_attribute(objects, attribute=attribute), key=score)[0]


def url_set_params(url, query):
    query_string = urlencode(query)
    parsed_url = urlparse(url)
    url = urlunparse(parsed_url._replace(query=query_string))
    return url
