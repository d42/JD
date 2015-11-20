from collections import namedtuple, UserList, Iterable

# from jakdojade.utils import fuzzy_search, resolve_class, dotted_lowercase_get
from jakdojade import utils


class TransitList(UserList):

    def search(self, value):
        return utils.fuzzy_search(self.data, value)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.data.__repr__())

    def __call__(self, value):
        return self.search(value)

    def __contains__(self, value):
        bool(self.search(value))


class TransitType:
    _json_prefix = ''
    _remaps = {}
    _recurse = {}

    def __init__(self, json):
        params = dict(self._transform_json(json))
        self._transform_children(params)
        self._set_slots(params)

    def _set_slots(self, params):

        for k, v in params.items():
            if k in self.__slots__:
                setattr(self, k, v)

    @classmethod
    def _transform_json(cls, json):
        for s in cls.__slots__:
            key = cls._remaps.get(s, cls._json_prefix + s)
            value = utils.dotted_lowercase_get(json, key)
            yield s, value

    def _transform_children(self, dictionary):
        for key, child_class in self._recurse.items():
            child_class = utils.resolve_class(child_class, globals())
            d_value = dictionary[key]

            if isinstance(d_value, Iterable):
                l = TransitList(child_class(d) for d in d_value)
                dictionary[key] = TransitList(l)
            else:
                dictionary[key] = child_class(d_value)


class City(TransitType):
    _search_attribute = 'name'
    _json_prefix = 'city'
    __slots__ = 'id', 'symbol', 'name', 'operators', 'position'
    _remaps = {'operators': 'cityTransportOperatorsArray',
               'position': 'cityCenterCoordinate'}
    _recurse = {'operators': 'Operator'}
    type_name = 'city'


class Operator(TransitType):
    _search_attribute = 'name'
    _json_prefix = 'transportOperator.transportOperator'
    __slots__ = 'id', 'name', 'symbol'
    type_name = 'operator'


class Stop(TransitType):
    _search_attribute = 'name'
    __slots__ = 'code', 'name', 'time_sum', 'lat', 'lon'
    _remaps = {'time_sum': 'travelMinsSum', 'lat': 'coordinate.y_lat',
               'lon': 'coordinate.x_lon'}
    type_name = 'stop'


class Line(TransitType):
    _search_attribute = 'name'
    _remaps = {'name': 'lineSymbol', 'routes': 'directions'}
    _recurse = {'routes': 'Route'}
    __slots__ = 'name', 'routes'
    _fields = __slots__
    type_name = 'line'



class Route(TransitType):
    _search_attribute = 'name'
    __slots__ = 'name', 'symbol', 'stops'
    _json_prefix = 'direction'
    _remaps = {'stops': 'mainStops'}
    _recurse = {'stops': 'Stop'}
    type_name = 'route'

    @property
    def geo_direction(self):
        start_lat, start_lon = self.stops[0].position
        end_lat, end_lon = self.stops[-1].position

        d_lat = start_lat - end_lat
        d_lon = start_lon - end_lon

        return d_lat, d_lon

    @property
    def geo_direction_name(self):
        d_lat, d_lon = self.geo_direction
        dest_1 = 'south' if d_lat > 0 else 'north'
        dest_2 = 'east' if d_lon > 0 else 'west'
        return [dest_1, dest_2]


TableEntry = namedtuple('TableEntry', 'hours minutes symbols')
