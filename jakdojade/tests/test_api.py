from ..types import City, TransitList
from .data import city_1, city_2


def test_list_search():
    l = TransitList()
    l.append(City(city_1))
    l.append(City(city_2))
    assert(l.search('bydgoszcz').name == 'Bydgoszcz')
