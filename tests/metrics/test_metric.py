import pytest
from toloka.metrics import TasksInPool


def test_initialize_with_sync_client(toloka_client):
    metric = TasksInPool('fake_pool', toloka_client=toloka_client)
    assert metric.atoloka_client.sync_client == toloka_client


def test_initialize_with_async_client(async_toloka_client):
    metric = TasksInPool('fake_pool', atoloka_client=async_toloka_client)
    assert metric.toloka_client == async_toloka_client.sync_client


def test_initialize_with_two_client(toloka_client, async_toloka_client):
    with pytest.raises(AssertionError):
        TasksInPool('fake_pool', toloka_client=toloka_client, atoloka_client=async_toloka_client)
