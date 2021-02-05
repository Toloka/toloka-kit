import pytest
from toloka.client import TolokaClient


@pytest.fixture
def toloka_client() -> TolokaClient:
    return TolokaClient('fake-token', 'SANDBOX')


@pytest.fixture
def toloka_url(toloka_client) -> str:
    return f'{toloka_client.url}/v1'


@pytest.fixture
def toloka_api_url(toloka_client) -> str:
    return f'{toloka_client.url}'
