import httpx
import pytest
import respx
from .backend_mock import BackendSearchMock


SOME_URL = 'http://some.url'


@pytest.fixture
def mock_items():
    return [
        {'pool_id': '1', 'id': 'X'},
        {'pool_id': '1', 'id': 'Y', 'created': None},
        {'pool_id': '1', 'id': 'Z'},
        {'pool_id': '1', 'id': 'A', 'created': '001'},
        {'pool_id': '1', 'id': 'B', 'created': '002'},
        {'pool_id': '1', 'id': 'C', 'created': '003'},
        {'pool_id': '2', 'id': 'E', 'created': '004'},
    ]


@pytest.mark.parametrize(
    ['params', 'expected'],
    [pytest.param({'pool_id': '1', 'sort': 'created'},
                  {'items': [{'pool_id': '1', 'id': 'X'},
                             {'pool_id': '1', 'id': 'Y', 'created': None}],
                   'has_more': True},
                  id='several-from-pool-1'),

     pytest.param({'pool_id': '2'},
                  {'items': [{'pool_id': '2', 'id': 'E', 'created': '004'}], 'has_more': False},
                  id='single-one-from-pool-2'),

     pytest.param({'created_gte': '002', 'created_lte': '002'},
                  {'items': [{'pool_id': '1', 'id': 'B', 'created': '002'}], 'has_more': False},
                  id='several-interval-conditions'),

     pytest.param({'id_gt': 'Z', 'id_lt': 'A'},
                  {'items': [], 'has_more': False},
                  id='no-such-items'),

     pytest.param({'sort': ['created', '-id'], 'limit': 5},
                  {'items': [{'pool_id': '1', 'id': 'Z'},
                             {'pool_id': '1', 'id': 'Y', 'created': None},
                             {'pool_id': '1', 'id': 'X'},
                             {'pool_id': '1', 'id': 'A', 'created': '001'},
                             {'pool_id': '1', 'id': 'B', 'created': '002'}],
                   'has_more': True},
                  id='reversed-sort')]
)
def test_backend_search_mock(mock_items, params, expected):
    backend_mock = BackendSearchMock(mock_items, limit=2)
    with respx.mock:
        respx.get(SOME_URL).mock(side_effect=backend_mock)
        response_json = httpx.get(SOME_URL, params=params).json()
        assert expected == response_json, response_json
        assert [expected] == backend_mock.responses


def test_backend_search_mock_change_storage(respx_mock, mock_items):
    backend_mock = BackendSearchMock(mock_items, limit=2)
    with respx.mock:
        respx.get(SOME_URL).mock(side_effect=backend_mock)

        response_json = httpx.get(SOME_URL, params={'sort': ['created'], 'created_gte': '004'}).json()
        assert {'items': [{'pool_id': '2', 'id': 'E', 'created': '004'}],
                'has_more': False} == response_json, response_json

        backend_mock.storage.append({'pool_id': '2', 'id': 'D', 'created': '005'})

        response_json = httpx.get(SOME_URL, params={'sort': ['created'], 'created_gte': '004'}).json()
        assert {'items': [{'pool_id': '2', 'id': 'E', 'created': '004'},
                          {'pool_id': '2', 'id': 'D', 'created': '005'}],
                'has_more': False} == response_json, response_json

        assert [
            {'items': [{'pool_id': '2', 'id': 'E', 'created': '004'}],
             'has_more': False},
            {'items': [{'pool_id': '2', 'id': 'E', 'created': '004'},
                       {'pool_id': '2', 'id': 'D', 'created': '005'}],
             'has_more': False},
        ] == backend_mock.responses
