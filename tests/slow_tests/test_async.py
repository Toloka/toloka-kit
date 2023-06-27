import asyncio
import sys
from threading import Thread

import pytest
from toloka.async_client import AsyncTolokaClient
from urllib3 import Retry


@pytest.mark.skipif((3, 7) <= sys.version_info < (3, 8), reason="Flaky on Python 3.7")
def test_async_client_survives_event_loop_change(internal_error_server_url, retries_before_response, fake_requester):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=internal_error_server_url,
        retryer_factory=lambda: Retry(retries_before_response, status_forcelist={500}, backoff_factor=0),
        retry_quotas=None,
        timeout=0.5,
    )

    loop = asyncio.get_event_loop()
    assert loop.run_until_complete(toloka_client.get_requester()) == fake_requester
    loop.close()
    loop = asyncio.new_event_loop()
    assert loop.run_until_complete(toloka_client.get_requester()) == fake_requester


def get_requester(result: list, client: AsyncTolokaClient):
    result.append(asyncio.run(client.get_requester()))


def test_async_client_can_be_multithreaded(internal_error_server_url, retries_before_response, fake_requester):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=internal_error_server_url,
        retryer_factory=lambda: Retry(retries_before_response, status_forcelist={500}, backoff_factor=0),
        retry_quotas=None,
        timeout=0.5,
    )
    result = []
    t1 = Thread(target=get_requester, args=(result, toloka_client))
    t2 = Thread(target=get_requester, args=(result, toloka_client))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert result == [fake_requester, fake_requester]
