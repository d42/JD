from durus.file_storage import FileStorage
from durus.connection import Connection, PersistentDict


def get_durus():
    if not hasattr(get_durus, 'connection'):
        get_durus.connection = Connection(FileStorage('cache.durus'))
    root = get_durus.connection.get_root()
    if 'requests' not in root:
        root['requests'] = PersistentDict()
    return root, get_durus.connection


def cached_request(func):
    def inner(self, url, params=None):
        root, connection = get_durus()
        params = params or {}
        attrs = url, tuple(sorted(params.items()))
        if attrs in root['requests']:
            r = root['requests'][attrs]
            return r
        return_value = func(self, url, params)
        if return_value.status_code == 200:
            root['requests'][attrs] = return_value
            connection.commit()
        return return_value
    return inner


def api_route(route):
    def inner(func):
        func.url = route
        return func
    return inner
