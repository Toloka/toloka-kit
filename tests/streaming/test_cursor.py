import asyncio
import inspect
import itertools
import pytest

from toloka.client import unstructure
from toloka.streaming.cursor import (
    _ByIdCursor,
    AssignmentCursor,
    BaseCursor,
    TaskCursor,
    UserBonusCursor,
    UserSkillCursor,
)
from ..testutils.backend_mock import BackendSearchMock


@pytest.fixture
def mocked_backend_for_user_bonus(requests_mock, toloka_url):
    backend = BackendSearchMock([], limit=RESPONSE_LIMIT)
    requests_mock.get(f'{toloka_url}/user-bonuses', json=backend)
    return backend


RESPONSE_LIMIT = 3


@pytest.fixture
def user_bonus_existing():
    return [
        {'user_id': '001', 'id': 'K', 'created': '2020-01-01T01:01:01'},  # 1
        {'user_id': '001', 'id': 'L', 'created': '2020-01-01T01:01:02'},  # 1, 2
        {'user_id': '001', 'id': 'M', 'created': '2020-01-01T01:01:02'},  # 1, 2
        {'user_id': '002', 'id': 'N', 'created': '2020-01-01T01:01:03'},  # 2, 3, 5
        {'user_id': '003', 'id': 'O', 'created': '2020-01-01T01:01:03'},  # 3, 5
        {'user_id': '003', 'id': 'P', 'created': '2020-01-01T01:01:03'},  # 3, 5
        {'user_id': '004', 'id': 'F', 'created': '2020-01-01T01:01:03'},  # 4
        {'user_id': '004', 'id': 'G', 'created': '2020-01-01T01:01:03'},  # 4
        {'user_id': '004', 'id': 'H', 'created': '2020-01-01T01:01:03'},  # 4
    ]


@pytest.fixture
def user_bonus_new():
    return [
        {'user_id': '007', 'id': 'Q', 'created': '2020-01-01T01:01:04'},  # 7
        {'user_id': '007', 'id': 'A', 'created': '2020-01-01T01:01:05'},  # 7
    ]


@pytest.fixture
def responses_by_existing_user_bonus():
    return [
        [
            {'user_id': '001', 'id': 'K', 'created': '2020-01-01T01:01:01'},  # 1
            {'user_id': '001', 'id': 'L', 'created': '2020-01-01T01:01:02'},  # 1, 2
            {'user_id': '001', 'id': 'M', 'created': '2020-01-01T01:01:02'},  # 1, 2
        ],
        [
            {'user_id': '001', 'id': 'L', 'created': '2020-01-01T01:01:02'},  # 1, 2
            {'user_id': '001', 'id': 'M', 'created': '2020-01-01T01:01:02'},  # 1, 2
            {'user_id': '002', 'id': 'N', 'created': '2020-01-01T01:01:03'},  # 2, 3, 5
        ],
        [
            {'user_id': '002', 'id': 'N', 'created': '2020-01-01T01:01:03'},  # 2, 3, 5
            {'user_id': '003', 'id': 'O', 'created': '2020-01-01T01:01:03'},  # 3, 5
            {'user_id': '003', 'id': 'P', 'created': '2020-01-01T01:01:03'},  # 3, 5
        ],
        [
            {'user_id': '004', 'id': 'F', 'created': '2020-01-01T01:01:03'},  # 4
            {'user_id': '004', 'id': 'G', 'created': '2020-01-01T01:01:03'},  # 4
            {'user_id': '004', 'id': 'H', 'created': '2020-01-01T01:01:03'},  # 4
        ],
        [
            {'user_id': '002', 'id': 'N', 'created': '2020-01-01T01:01:03'},  # 2, 3, 5
            {'user_id': '003', 'id': 'O', 'created': '2020-01-01T01:01:03'},  # 3, 5
            {'user_id': '003', 'id': 'P', 'created': '2020-01-01T01:01:03'},  # 3, 5
        ],
        [],
    ]


@pytest.fixture
def responses_after_new_user_bonus():
    return [
        [
            {'user_id': '007', 'id': 'Q', 'created': '2020-01-01T01:01:04'},  # 7
            {'user_id': '007', 'id': 'A', 'created': '2020-01-01T01:01:05'},  # 7
        ]
    ]


def _keep_items_only(responses):
    return [response['items'] for response in responses]


def fetch_sync(cursor):
    return unstructure([item for item in cursor])


def fetch_async(cursor):
    async def _fetch():
        return [item async for item in cursor]

    loop = asyncio.get_event_loop()
    return unstructure(loop.run_until_complete(_fetch()))


@pytest.mark.parametrize('fetcher', [fetch_sync, fetch_async])
def test_cursor_create_expanded(toloka_client, mocked_backend_for_user_bonus, user_bonus_existing, fetcher):
    mocked_backend_for_user_bonus.storage.extend(user_bonus_existing)
    cursor = UserBonusCursor(user_id='002', toloka_client=toloka_client)
    assert [{
        'user_bonus': {'user_id': '002', 'id': 'N', 'created': '2020-01-01T01:01:03'},
        'event_time': '2020-01-01T01:01:03',
    }] == fetcher(cursor)
    assert [] == fetcher(cursor)


@pytest.mark.parametrize(
    ['fetcher', 'add_new'],
    itertools.product((fetch_sync, fetch_async), (False, True))
)
def test_cursor_iter(
    toloka_client,
    mocked_backend_for_user_bonus,
    user_bonus_existing,
    responses_by_existing_user_bonus,
    user_bonus_new,
    responses_after_new_user_bonus,
    fetcher,
    add_new,
):
    mocked_backend_for_user_bonus.storage.extend(user_bonus_existing)
    cursor = UserBonusCursor(toloka_client=toloka_client)

    # It should return all existing user bonuses.
    assert [
        {'user_bonus': item, 'event_time': item['created']}
        for item in user_bonus_existing
    ] == fetcher(cursor)
    # Check requests sequence.
    assert responses_by_existing_user_bonus == _keep_items_only(mocked_backend_for_user_bonus.responses)

    if add_new:
        mocked_backend_for_user_bonus.storage.extend(user_bonus_new)
        assert [
            {'user_bonus': item, 'event_time': item['created']}
            for item in user_bonus_new
        ] == fetcher(cursor)
        assert (
            responses_by_existing_user_bonus + responses_after_new_user_bonus
        ) == _keep_items_only(mocked_backend_for_user_bonus.responses)
    else:
        assert [] == fetcher(cursor)
        assert responses_by_existing_user_bonus + [[]] == _keep_items_only(mocked_backend_for_user_bonus.responses)


@pytest.mark.parametrize('chunk_size', range(1, 9))
def test_cursor_iter_different_chunk_size(toloka_client, mocked_backend_for_user_bonus, user_bonus_existing, chunk_size):
    mocked_backend_for_user_bonus.storage.extend(user_bonus_existing)
    mocked_backend_for_user_bonus.limit = chunk_size
    cursor = UserBonusCursor(toloka_client=toloka_client)
    # Sort order may change due to homogenous requests (sorted by id with fixed time).
    assert sorted([
        {'user_bonus': item, 'event_time': item['created']}
        for item in user_bonus_existing
    ], key=str) == sorted(unstructure(list(cursor)), key=str)


@pytest.mark.parametrize('chunk_size', range(1, 9))
def test_cursor_iter_by_one(toloka_client, mocked_backend_for_user_bonus, user_bonus_existing, chunk_size):
    mocked_backend_for_user_bonus.storage.extend(user_bonus_existing)
    mocked_backend_for_user_bonus.limit = chunk_size
    cursor = UserBonusCursor(toloka_client=toloka_client)

    result = []
    for _ in range(len(user_bonus_existing) + 1):  # Iterate one more time to check no more items fetched.
        item = next(iter(cursor), None)
        if item and len(result) <= len(user_bonus_existing):
            result.append(item)
        else:
            break

    assert sorted([
        {'user_bonus': item, 'event_time': item['created']}
        for item in user_bonus_existing
    ], key=str) == sorted(unstructure(result), key=str)


def test_assignment_cursor(requests_mock, toloka_url, toloka_client):
    backend_data = [
        {'pool_id': '100', 'id': 'A', 'submitted': '2020-01-01T01:01:01'},
        {'pool_id': '100', 'id': 'B', 'submitted': '2020-01-01T01:01:02', 'accepted': '2020-01-01T01:01:03'},
    ]
    backend = BackendSearchMock(backend_data)
    requests_mock.get(f'{toloka_url}/assignments', json=backend)

    cursor_submitted = AssignmentCursor(pool_id='100', event_type='SUBMITTED', toloka_client=toloka_client)
    assert [
        {'assignment': item, 'event_type': 'SUBMITTED', 'event_time': item['submitted']}
        for item in backend_data
    ] == unstructure(list(cursor_submitted))

    cursor_accepted = AssignmentCursor(pool_id='100', event_type='ACCEPTED', toloka_client=toloka_client)
    assert [{
        'assignment': {'pool_id': '100', 'id': 'B', 'submitted': '2020-01-01T01:01:02', 'accepted': '2020-01-01T01:01:03'},
        'event_type': 'ACCEPTED',
        'event_time': '2020-01-01T01:01:03',
    }] == unstructure(list(cursor_accepted))


@pytest.mark.parametrize('chunk_size', range(1, 4))
def test_task_cursor(requests_mock, toloka_url, toloka_client, chunk_size):
    backend_data = [
        {'pool_id': '100', 'id': 'A', 'created': '2020-01-01T01:01:01'},
        {'pool_id': '100', 'id': 'B', 'created': '2020-01-01T01:01:02'},
        {'pool_id': '100', 'id': 'C', 'created': '2020-01-01T01:01:03'},
    ]
    backend = BackendSearchMock(backend_data, limit=chunk_size)
    requests_mock.get(f'{toloka_url}/tasks', json=backend)

    cursor = TaskCursor(pool_id='100', toloka_client=toloka_client)
    assert [
        {'task': item, 'event_time': item['created']}
        for item in backend_data
    ] == unstructure(list(cursor))


@pytest.mark.parametrize(
    ['chunk_size', 'event_type'],
    itertools.product(range(1, 4), ['CREATED', 'MODIFIED'])
)
def test_user_skill_cursor(requests_mock, toloka_url, toloka_client, chunk_size, event_type):
    backend_data = [
        {'user_id': '001', 'id': 'A', 'created': '2020-01-01T01:01:01', 'modified': '2020-01-01T01:01:01'},
        {'user_id': '001', 'id': 'B', 'created': '2020-01-01T01:01:02', 'modified': '2020-01-01T01:01:02'},
        {'user_id': '001', 'id': 'C', 'created': '2020-01-01T01:01:03', 'modified': '2020-01-01T01:01:03'},
    ]
    backend = BackendSearchMock(backend_data, limit=chunk_size)
    requests_mock.get(f'{toloka_url}/user-skills', json=backend)

    cursor = UserSkillCursor(event_type=event_type, toloka_client=toloka_client)
    assert [
        {'user_skill': item, 'event_type': event_type, 'event_time': item[event_type.lower()]}
        for item in backend_data
    ] == unstructure(list(cursor))


@pytest.mark.parametrize(
    ['object_class', 'async_to_sync_differencies'],
    [
        (
            _ByIdCursor,
            {'await ensure_async(self.fetcher)': 'self.fetcher'}
        ),
        (
            BaseCursor,
            {
                'await ensure_async(fetcher)': 'fetcher',
                'async for item in _ByIdCursor': 'for item in _ByIdCursor',
            }
        ),
    ]
)
def test_exact_iter_and_aiter_code(object_class, async_to_sync_differencies):
    def get_func_body(func):
        return '\n'.join(inspect.getsource(func).rstrip().split('\n')[1:])

    iter_code = get_func_body(object_class.__iter__)
    aiter_code = get_func_body(object_class.__aiter__)
    for async_version, sync_version in async_to_sync_differencies.items():
        aiter_code = aiter_code.replace(async_version, sync_version)

    assert iter_code.split('\n') == aiter_code.split('\n')
