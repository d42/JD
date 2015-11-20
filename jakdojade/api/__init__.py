
from .constants import urls
from jakdojade.settings import settings as s
from jakdojade.oauth import OauthRequests
from jakdojade.decorators import api_route
from jakdojade.types import City, TransitList, Line
from jakdojade.utils import DeferredType


class RawApi:
    def __init__(self, req=OauthRequests):
        self.req = (req(s.SECRET_KEY, s.CLIENT_KEY)
                    if isinstance(req, type) else req)

    @api_route(urls.cities_v3)
    def cities(self):
        """ returns cities, city ids and operators """
        return self.req(self.cities.url).json()

    @api_route(urls.line_stops_v2)
    def routes(self, city_id, operator_id, line_symbol):
        params = {'cid': city_id,
                  'operatorId': operator_id,
                  'lineSymbol': line_symbol}
        return self.req(self.routes.url, params=params).json()

    @api_route(urls.schedule_v2)
    def timetable(self, line, stop, direction_id):
        params = {'cid': self.city,
                  'operatorId': self.operator,
                  'lineSymbol': line,
                  'dirSymbol': direction_id,
                  'stopCode': stop}
        return self.req(self.timetable.url, params=params).json()

    @api_route(urls.days_codes)
    def days_codes(self, city_id):
        params = {'cid': city_id}
        return self.req(self.days_codes.url, params=params).json()

    @api_route(urls.status)
    def status(self, city_id):
        params = {'cid': city_id, 'globalMessages': 'true'}
        return self.req(self.status.url, params=params).json()

    @api_route(urls.all_lines_v3)
    def city_lines(self, city_symbol):
        params = {'citySymbol': city_symbol}
        return self.req(self.city_lines.url, params=params).json()


class ObjectApi:
    def __init__(self, raw_api=RawApi):
        self.api = raw_api() if isinstance(raw_api, type) else raw_api

    def cities(self):
        ':rtype: [City]'
        json = self.api.cities()
        return TransitList(City(j) for j in json['citiesArray'])

    def line(self, city, operator, line_symbol):
        json = self.api.routes(city.id, operator.id, line_symbol)
        return Line(json)

    def lines(self, city, operator):
        def get_op_id(operator_json):
            return operator_json['transportOperator']['transportOperatorId']

        json = self.api.city_lines(city.symbol)
        ops_list = json['transportOperatorsArray']
        op_dict = next((op for op in ops_list if get_op_id(op) == operator.id),
                       {'linesArray': []})
        return [(DeferredType(
            name=line['lineName'],
            _req=self.line, _args=[city, operator, line['lineName']]))
                for line in op_dict['linesArray']]


