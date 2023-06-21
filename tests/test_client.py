import copy
import pickle
import ssl
from decimal import Decimal

import httpx
import pytest
import simplejson
import toloka.client as client
from pytest_lazyfixture import lazy_fixture
from toloka.client import TolokaClient

from .conftest import SyncOverAsyncTolokaClient
from .testutils.util_functions import check_headers


@pytest.fixture
def random_url():
    return 'https://testing.toloka.yandex.ru'


def test_client_create_exceptions(random_url):
    with pytest.raises(ValueError):
        TolokaClient('fake-token', 'SANDBOX', url=random_url)
    with pytest.raises(ValueError):
        TolokaClient('fake-token')


def test_client_pickleable(random_url):
    toloka_client = TolokaClient('fake-token', 'SANDBOX')
    dumped = pickle.dumps(toloka_client)  # Check that it's possible.
    loaded = pickle.loads(dumped)
    assert loaded


def test_async_client_pickleable(async_toloka_client):
    dumped = pickle.dumps(async_toloka_client)
    loaded = pickle.loads(dumped)
    assert loaded


@pytest.fixture
def requester_mapping():
    return {
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


def test_different_urls(respx_mock, random_url, requester_mapping):

    def get_requester(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_requester',
            'X-Low-Level-Method': 'get_requester',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(requester_mapping), status_code=200)

    respx_mock.get(f'{random_url}/api/v1/requester').mock(side_effect=get_requester)

    toloka_client = TolokaClient('fake-token', url=random_url)
    requester = toloka_client.get_requester()
    assert requester_mapping == client.unstructure(requester)

    toloka_client = TolokaClient('fake-token', url=f'{random_url}/')
    requester = toloka_client.get_requester()
    assert requester_mapping == client.unstructure(requester)


@pytest.fixture
def shared_account_id():
    return '123'


@pytest.fixture
def client_act_under_account_sync(random_url, shared_account_id):
    return TolokaClient('fake-token', url=random_url, act_under_account_id=shared_account_id)


@pytest.fixture(params=[True, False])
def client_act_under_account_async(client_act_under_account_sync, request):
    return SyncOverAsyncTolokaClient(
        sync_client=client_act_under_account_sync, use_async_gen_adapter_as_gen=request.param
    )


@pytest.fixture(params=[lazy_fixture('client_act_under_account_sync'), lazy_fixture('client_act_under_account_async')])
def client_act_under_account(request) -> TolokaClient:
    return request.param


def test_client_act_as(respx_mock, client_act_under_account, shared_account_id, requester_mapping):

    def get_requester(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(
                client_act_under_account, client.TolokaClient
            ) else 'async_client',
            'X-Top-Level-Method': 'get_requester',
            'X-Low-Level-Method': 'get_requester',
            'X-Act-Under-Account-ID': shared_account_id
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(requester_mapping), status_code=200)

    respx_mock.get(f'{client_act_under_account.url}/api/v1/requester').mock(side_effect=get_requester)

    client_act_under_account.get_requester()


def get_verify_mode(client: TolokaClient):
    return client._session._transport_for_url(client.url)._pool._ssl_context.verify_mode


@pytest.mark.parametrize(
    'verify,expected_ssl_context',
    [
        (True, ssl.CERT_REQUIRED),
        (False, ssl.CERT_NONE),
    ]
)
def test_client_ssl_verify(toloka_client, verify, expected_ssl_context):
    client = copy.deepcopy(toloka_client)
    client.verify = verify
    assert get_verify_mode(client) == expected_ssl_context


@pytest.mark.parametrize(
    'token,is_apikey', [
        ('fake-token', False),
        (
            # api-key like fake token
            'LrB_oHKYMtXeD-BoVFWTwi.nfNC.vcRjfXLoJtfWAExAizBKrsBlbfLQJFSFDEnoUODffGsyPjpOlfyAIkFlgZBloBQJHxkjMtAohTTCm-sVtAnNueMVEGqiyBPxz-elOp-hEpA',
            True
        )
    ]
)
def test_client_auth_headers(respx_mock, token, is_apikey):
    client = TolokaClient(environment='SANDBOX', token=token)

    def get_requester(request):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_requester',
            'X-Low-Level-Method': 'get_requester',
            'authorization': f'ApiKey {token}' if is_apikey else f'OAuth {token}',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps({}), status_code=200)

    respx_mock.get(f'{client.url}/api/v1/requester').mock(side_effect=get_requester)
    client.get_requester()
