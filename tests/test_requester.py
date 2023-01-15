from decimal import Decimal

import httpx
import simplejson
import toloka.client as client

from .testutils.util_functions import check_headers


def test_get_requester(respx_mock, toloka_client, toloka_url):
    result = {
        'id': '566ec2b0ff0deeaae5f9d500',
        'balance': Decimal('120.3'),
        'public_name': {
            'EN': 'John Smith',
            'RU': 'Джон Смит',
        },
        'company': {
            'id': '1',
            'superintendent_id': 'superintendent-1id',
        },
    }

    def get_requester(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_requester',
            'X-Low-Level-Method': 'get_requester',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(result), status_code=200)

    respx_mock.get(f'{toloka_url}/requester').mock(side_effect=get_requester)
    requester = toloka_client.get_requester()
    assert result == client.unstructure(requester)
    assert requester.balance == Decimal('120.3')
