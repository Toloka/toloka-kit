import attr
from toloka.client._converter import structure, unstructure
from toloka.client.search_requests import SortOrder, SearchRequestMetaclass, BaseSortItems
from typing import Optional


class SearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        x: str
        y: int

    z: Optional[bool] = None


SortItems = BaseSortItems.for_fields('SortItems', ['a', 'b', 'y'])
SortItem = SortItems.SortItem
SortField = SortItem.SortField


def test_attributes():
    assert {
        ('x_lt', Optional[str], None),
        ('x_lte', Optional[str], None),
        ('x_gt', Optional[str], None),
        ('x_gte', Optional[str], None),
        ('y_lt', Optional[int], None),
        ('y_lte', Optional[int], None),
        ('y_gt', Optional[int], None),
        ('y_gte', Optional[int], None),
        ('z', Optional[bool], None),
    } == set((f.name, f.type, f.default) for f in attr.fields(SearchRequest))


def test_sort_field():

    sort = SortItems(items=[
        SortItem(SortField.A, SortOrder.ASCENDING),
        SortItem(SortField.Y, SortOrder.DESCENDING),
    ])

    assert sort == structure('a,-y', SortItems)
    assert sort == structure(['a', '-y'], SortItems)
    assert sort == structure(sort, SortItems)
    assert 'a,-y' == unstructure(sort)

    assert 'b,-a,y' == unstructure(SortItems('b,-a,y'))
    assert '-a,b' == unstructure(SortItems(['-a', 'b']))
    assert '-y' == unstructure(SortItems([SortItem(SortField.Y, SortOrder.DESCENDING)]))
