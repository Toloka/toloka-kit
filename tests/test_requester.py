from decimal import Decimal

import simplejson
import toloka.client as client


def test_get_requester(requests_mock, toloka_client, toloka_url):
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

    requests_mock.get(f'{toloka_url}/requester', text=simplejson.dumps(result))
    requester = toloka_client.get_requester()
    assert result == client.unstructure(requester)
    assert requester.balance == Decimal('120.3')
