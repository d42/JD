from jakdojade.types import TransitList, Operator, Line
from jakdojade.utils import PassthroughMixin
from jakdojade.api import ObjectApi

__all__ = ['JakDojade']


class GnujFactory:
    def __init__(self, parent, api):
        self.api = api
        self.parent = parent

    def city(self, *args):
        return OCity(*args, _parent=self.parent, _api=self.api)

    def operator(self, *args):
        return OOperator(*args, _parent=self.parent, _api=self.api)

    def line(self, *args):
        return OLine(*args, _parent=self.parent, _api=self.api)

    def route(self, *args):
        return ORoute(*args, _parent=self.parent, _api=self.api)

    def stop(self, *args):
        return OStop(*args, _parent=self.parent, _api=self.api)


class JakDojade:
    def __init__(self, api=ObjectApi):
        self.api = api() if isinstance(api, type) else api
        self.factory = GnujFactory(self, self.api)

    @property
    def cities(self):
        cities = self.api.cities()
        return TransitList(self.factory.city(c) for c in cities)

    def city(self, city_name):
        ':rtype: OCity'
        return self.cities.search(city_name)


class StateReader:
    __slots__ = 'cache', 'node'

    def __init__(self, node):
        self.cache = {}
        self.node = node

    def __getattr__(self, attr):
        attr = attr.lower()
        for n in self.node_path:
            name = n.type_name.lower()
            if attr == name:
                return n

    @property
    def node_path(self):
        node = self.node
        while node.parent:
            yield node
            node = node.parent


class ORMType(PassthroughMixin):
    def __init__(self, data, _parent, _api):
        ''':type _api: RawApi'''
        self.data = data
        self.api = _api
        self.factory = GnujFactory(self, _api)
        self.parent = _parent
        self.state = StateReader(self)


class OCity(ORMType):

    @property
    def operators(self):
        return TransitList(self.factory.operator(o)
                           for o in self.data.operators)

    def operator(self, symbol):
        ':rtype: Operator'
        return self.factory.operator(self.data.operators(symbol))


class OOperator(ORMType):

    @property
    def lines(self):
        return TransitList(self.factory.line(l)
                           for l in self.api.lines(self.state.city, self))

    def line(self, line_symbol):
        ':rtype: Line'
        line = self.api.line(self.state.city, self.state.operator, line_symbol)
        return self.factory.line(line)

    def __repr__(self):
        return '<{} {s.name} ({s.id}:{s.symbol})>'.format(self.__class__.__name__, s=self)


class OLine(ORMType):

    @property
    def routes(self):
        return TransitList(self.factory.route(r) for r in self.data.routes)

    def __repr__(self):
        return '<{} {s.name}>'.format(self.__class__.__name__, s=self)


class ORoute(ORMType):

    @property
    def stops(self):
        return TransitList(self.factory.stop(s) for s in self.data.stops)

    def stop(self, name):
        'rtype: jakdojade.types.Stop'
        return self.stops(name)

    def __repr__(self):
        return '<{} {s.parent.name} -> {s.name}>'.format(self.__class__.__name__, s=self)



class OStop(ORMType):

    @property
    def destination(self):
        pass

    def __repr__(self):
        return '<{} {s.code}:{s.name} ({s.lat}, {s.lon})>'.format(self.__class__.__name__, s=self)
