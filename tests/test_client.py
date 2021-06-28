from decimal import Decimal

import pytest
import simplejson

from toloka.client import TolokaClient
import toloka.client as client


@pytest.fixture
def random_url():
    return 'https://testing.toloka.yandex.ru'


def test_client_create_exceptions(random_url):
    with pytest.raises(ValueError):
        TolokaClient('fake-token', 'SANDBOX', url=random_url)
    with pytest.raises(ValueError):
        TolokaClient('fake-token')


def test_different_urls(requests_mock, random_url):
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

    requests_mock.get(f'{random_url}/api/v1/requester', text=simplejson.dumps(result))

    toloka_client = TolokaClient('fake-token', url=random_url)
    requester = toloka_client.get_requester()
    assert result == client.unstructure(requester)

    toloka_client = TolokaClient('fake-token', url=f'{random_url}/')
    requester = toloka_client.get_requester()
    assert result == client.unstructure(requester)
