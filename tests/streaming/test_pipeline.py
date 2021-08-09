import asyncio
import datetime
import pytest

from toloka.client import unstructure
from toloka.streaming import AssignmentsObserver, AsyncMultithreadWrapper, PoolStatusObserver, Pipeline

from ..testutils.backend_mock import BackendSearchMock


@pytest.fixture
def existing_backend_assignments():
    return [
        {'pool_id': '100', 'id': 'K', 'submitted': '2020-01-01T01:01:01', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'L', 'submitted': '2020-01-01T01:01:01', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'M', 'submitted': '2020-01-01T01:01:01', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'N', 'submitted': '2020-01-01T01:01:02', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'O', 'submitted': '2020-01-01T01:01:02', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'P', 'submitted': '2020-01-01T01:01:02', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'B', 'submitted': '2020-01-01T01:01:03', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'A', 'submitted': '2020-01-01T01:01:04', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'Z', 'created': '2020-01-01T01:01:01', 'status': 'ACTIVE'},
    ]


@pytest.fixture
def new_backend_assignments():
    return [
        {'pool_id': '100', 'id': 'C', 'submitted': '2020-01-01T01:01:05', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'D', 'submitted': '2020-01-01T01:01:06', 'status': 'SUBMITTED'},
    ]


@pytest.mark.parametrize('use_async', [False, True])
def test_pipeline(requests_mock, toloka_url, toloka_client, existing_backend_assignments, new_backend_assignments, use_async):
    pool_mock = {'id': '100', 'status': 'OPEN'}

    backend = BackendSearchMock(existing_backend_assignments, limit=3)
    requests_mock.get(f'{toloka_url}/assignments', json=backend)
    requests_mock.get(f'{toloka_url}/pools/100', json=pool_mock)

    save_submitted_here = []
    save_pool_info_here = []

    def handle_submitted(events):
        save_submitted_here.extend(event.assignment for event in events)

    def handle_pool_open(pool):
        active_count = len(list(toloka_client.get_assignments(pool_id=pool.id, status='ACTIVE')))
        save_pool_info_here.append(f'pool open with active tasks count: {active_count}')

    def handle_pool_close(pool):
        save_pool_info_here.append(f'pool closed with reason: {pool.last_close_reason.value}')

    async def _add_new_assignments(after_sec):
        await asyncio.sleep(after_sec)
        backend.storage.extend(new_backend_assignments)

    async def _expire_active_and_close_pool(after_sec):
        await asyncio.sleep(after_sec)
        for item in backend.storage:
            if item['status'] == 'ACTIVE':
                item['status'] = 'EXPIRED'
        pool_mock['status'] = 'CLOSED'
        pool_mock['last_close_reason'] = 'EXPIRED'

    _toloka_client = AsyncMultithreadWrapper(toloka_client) if use_async else toloka_client

    pipeline = Pipeline(datetime.timedelta(milliseconds=500))
    pipeline.register(AssignmentsObserver(_toloka_client, pool_id='100')).on_submitted(handle_submitted)
    pool_observer = pipeline.register(PoolStatusObserver(_toloka_client, pool_id='100'))
    pool_observer.on_open(handle_pool_open)
    pool_observer.on_closed(handle_pool_close)

    async def _main():
        await asyncio.wait(list(map(asyncio.create_task, (
            pipeline.run(),
            _add_new_assignments(after_sec=1),
            _expire_active_and_close_pool(after_sec=2),
        ))))

    asyncio.run(_main())

    expected_saved = [item for item in backend.storage if item.get('submitted')]
    assert expected_saved == unstructure(save_submitted_here)

    assert [
        'pool open with active tasks count: 1',
        'pool closed with reason: EXPIRED',
    ] == save_pool_info_here
