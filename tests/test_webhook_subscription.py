import datetime
from urllib.parse import urlparse, parse_qs
from uuid import uuid4

import pytest
import toloka.client as client


@pytest.fixture
def webhook_subscriptions_map():
    return [
        {
            'webhook_url': 'https://awesome-requester.com/toloka-webhook',
            'event_type': 'ASSIGNMENT_CREATED',
            'pool_id': '121212'
        },
        {
            'webhook_url': 'https://awesome-requester.com/toloka-webhook',
            'event_type': 'POOL_CLOSED',
            'pool_id': '121212'
        },
        {    # Raises a validation_errors.
            'event_type': 'POOL_CLOSED',
            'pool_id': '121212'
        }
    ]


@pytest.fixture
def upsert_webhook_subscriptions_result_map():
    return {
        'items': {
            '0': {
                'webhook_url': 'https://awesome-requester.com/toloka-webhook',
                'event_type': 'ASSIGNMENT_CREATED',
                'pool_id': '121212',
                'id': 'webhook-subscription-0',
                'created': '2016-10-09T11:42:01'
            },
            '1': {
                'webhook_url': 'https://awesome-requester.com/toloka-webhook',
                'event_type': 'POOL_CLOSED',
                'pool_id': '121212',
                'id': 'webhook-subscription-1',
                'created': '2016-10-09T11:42:01'
            }
        },
        'validation_errors': {
            '2': {
                'webhook_url': {
                    'code': 'VALUE_REQUIRED',
                    'message': 'May not be null'
                }
            }
        }
    }


def test_upsert_webhook_subscriptions(
    requests_mock, toloka_client, toloka_url,
    webhook_subscriptions_map, upsert_webhook_subscriptions_result_map
):

    def upsert_webhook_subscriptions_mock(request, _):
        assert webhook_subscriptions_map == request.json()
        return upsert_webhook_subscriptions_result_map

    # upsert_webhook_subscriptions -> operation
    requests_mock.put(f'{toloka_url}/webhook-subscriptions', json=upsert_webhook_subscriptions_mock, status_code=201)

    result = toloka_client.upsert_webhook_subscriptions(webhook_subscriptions_map)
    assert upsert_webhook_subscriptions_result_map == client.unstructure(result)


@pytest.fixture
def webhook_subscription_map():
    return {
        'webhook_url': 'https://awesome-requester.com/toloka-webhook',
        'event_type': 'ASSIGNMENT_CREATED',
        'pool_id': '121212',
        'id': 'webhook-subscription-1',
        'created': '2016-10-09T11:42:01'
    }


def test_get_webhook_subscription(requests_mock, toloka_client, toloka_url, webhook_subscription_map):
    requests_mock.get(f'{toloka_url}/webhook-subscriptions/webhook_subscription-1', json=webhook_subscription_map)
    result = toloka_client.get_webhook_subscription('webhook_subscription-1')
    assert webhook_subscription_map == client.unstructure(result)


def test_get_webhook_subscriptions(requests_mock, toloka_client, toloka_url, webhook_subscription_map):
    webhook_subscriptions = [
        dict(
            webhook_subscription_map,
            id=str(uuid4()),
            created=datetime.datetime(2016, 10, 9, 11, 42, sec).strftime('%Y-%m-%dT%H:%M:%S')
        )
        for sec in range(50)
    ]

    def get_webhook_subscriptions_mock(request, _):
        params = parse_qs(urlparse(request.url).query)
        created_gt = params.pop('created_gt')[0] if 'created_gt' in params else None
        assert {
            'event_type': ['ASSIGNMENT_CREATED'],
            'pool_id': ['121212'],
            'sort': ['created']
        } == params, params

        items = [
            webhook_subscription
            for webhook_subscription in webhook_subscriptions
            if created_gt is None or webhook_subscription['created'] > created_gt
        ][:3]
        return {'items': items, 'has_more': items[-1]['created'] != webhook_subscriptions[-1]['created']}

    requests_mock.get(f'{toloka_url}/webhook-subscriptions', json=get_webhook_subscriptions_mock)

    # Request object syntax
    request = client.search_requests.WebhookSubscriptionSearchRequest(
        event_type='ASSIGNMENT_CREATED',
        pool_id=121212,
    )
    result = toloka_client.get_webhook_subscriptions(request)
    assert webhook_subscriptions == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_webhook_subscriptions(
        event_type='ASSIGNMENT_CREATED',
        pool_id=121212,
    )
    assert webhook_subscriptions == client.unstructure(list(result))
