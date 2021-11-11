import random
import uuid

import pytest
from toloka.client import TolokaClient


@pytest.fixture
def toloka_client() -> TolokaClient:
    return TolokaClient('fake-token', 'SANDBOX')


@pytest.fixture
def toloka_client_prod() -> TolokaClient:
    return TolokaClient('fake-token', 'PRODUCTION')


@pytest.fixture
def toloka_api_url(toloka_client) -> str:
    return f'{toloka_client.url}/api'


@pytest.fixture
def toloka_url(toloka_api_url) -> str:
    return f'{toloka_api_url}/v1'


@pytest.fixture
def toloka_app_url(toloka_client_prod) -> str:
    return f'{toloka_client_prod.url}/api/app/v0'


@pytest.fixture
def no_uuid_random():
    rd = random.Random()
    rd.seed(0)
    uuid.uuid4 = lambda: uuid.UUID(int=rd.getrandbits(128))
