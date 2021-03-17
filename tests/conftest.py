import pytest
import random
from toloka.client import TolokaClient
import uuid


@pytest.fixture
def toloka_client() -> TolokaClient:
    return TolokaClient('fake-token', 'SANDBOX')


@pytest.fixture
def toloka_url(toloka_client) -> str:
    return f'{toloka_client.url}/v1'


@pytest.fixture
def toloka_api_url(toloka_client) -> str:
    return f'{toloka_client.url}'


@pytest.fixture
def no_uuid_random():
    rd = random.Random()
    rd.seed(0)
    uuid.uuid4 = lambda: uuid.UUID(int=rd.getrandbits(128))
