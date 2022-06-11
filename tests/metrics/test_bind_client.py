import pytest

from toloka.metrics import BaseMetric, bind_client
from pytest_lazyfixture import lazy_fixture


@pytest.fixture
def base_metrics_list():
    return [BaseMetric() for _ in range(10)]


@pytest.mark.parametrize(
    'client', [
        lazy_fixture('toloka_client'),
        lazy_fixture('async_toloka_client'),
    ]
)
def test_client_is_shared(client, base_metrics_list):
    bind_client(base_metrics_list, client)
    sync_client = base_metrics_list[0].toloka_client
    async_client = base_metrics_list[0].atoloka_client
    assert sync_client and async_client
    for metric in base_metrics_list[1:]:
        assert metric.toloka_client == sync_client
        assert metric.atoloka_client == async_client
