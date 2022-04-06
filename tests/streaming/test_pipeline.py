import asyncio
import attr
import copy
import datetime
import logging
import pytest
from typing import List, Set, Tuple

from toloka.client import unstructure
from toloka.util.async_utils import ComplexException, AsyncMultithreadWrapper
from toloka.streaming import Pipeline
from toloka.streaming.observer import AssignmentsObserver, BaseObserver, PoolStatusObserver
from toloka.streaming.storage import JSONLocalStorage
from toloka.streaming.locker import NewerInstanceDetectedError

from ..testutils.backend_mock import BackendSearchMock


Pipeline.MIN_SLEEP_SECONDS = 0


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


@pytest.fixture
def new_backend_assignments_after_restore():
    return [
        {'pool_id': '100', 'id': 'E', 'submitted': '2020-01-01T01:01:07', 'status': 'SUBMITTED'},
        {'pool_id': '100', 'id': 'F', 'submitted': '2020-01-01T01:01:08', 'status': 'SUBMITTED'},
    ]


def test_pipeline_errored_callback(requests_mock, toloka_url, toloka_client, existing_backend_assignments):
    storage = [item for item in existing_backend_assignments if item['status'] != 'ACTIVE']  # Make sure it stops.
    assert storage  # Check this test uses correct data.

    backend = BackendSearchMock(storage, limit=3)  # Chunk size doesn't make sense here.
    requests_mock.get(f'{toloka_url}/assignments', json=backend)
    requests_mock.get(f'{toloka_url}/pools/100', json={'id': '100', 'status': 'CLOSED'})

    class HandlerRaiseSometimes:
        def __init__(self):
            self.calls_count = 0
            self.received = []

        def __call__(self, events):
            self.calls_count += 1
            if self.calls_count % 2:
                raise ValueError('Raised from callback')
            self.received.extend(events)

    pipeline = Pipeline(datetime.timedelta(milliseconds=100))
    observer = pipeline.register(AssignmentsObserver(toloka_client, pool_id='100'))
    handler = observer.on_submitted(HandlerRaiseSometimes())

    loop = asyncio.new_event_loop()

    with pytest.raises(ComplexException) as exc:
        loop.run_until_complete(pipeline.run())
    assert 'Raised from callback' in str(exc)
    assert 1 == handler.calls_count
    assert [] == handler.received

    loop.run_until_complete(pipeline.run())
    assert 2 == handler.calls_count
    events_expected = [{'assignment': item, 'event_type': 'SUBMITTED', 'event_time': item['submitted']}
                       for item in storage]
    assert events_expected == unstructure(handler.received)


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

    async def handle_pool_open(pool):
        active_count = len(list(toloka_client.get_assignments(pool_id=pool.id, status='ACTIVE')))
        save_pool_info_here.append(f'pool open with active tasks count: {active_count}')

    class HandlePoolClose:
        async def __call__(self, pool):
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
    pool_observer.on_closed(HandlePoolClose())

    async def _main():
        loop = asyncio.get_event_loop()
        await asyncio.wait(list(map(loop.create_task, (
            pipeline.run(),
            _add_new_assignments(after_sec=1),
            _expire_active_and_close_pool(after_sec=2),
        ))))

    asyncio.new_event_loop().run_until_complete(_main())

    expected_saved = [item for item in backend.storage if item.get('submitted')]
    assert expected_saved == unstructure(save_submitted_here)

    assert [
        'pool open with active tasks count: 1',
        'pool closed with reason: EXPIRED',
    ] == save_pool_info_here


def test_inject(toloka_client):

    def handler_func():
        pass

    async def handler_async_func():
        pass

    @attr.s
    class HandlerClass:
        w = attr.ib()
        x = attr.ib()

        def __call__(self, *args):
            pass

    @attr.s
    class HandlerClassCustomInject:
        y = attr.ib()
        z = attr.ib()

        def inject(self, injection):
            self.y = injection.y

        def __call__(self, *args):
            pass

    toloka_client_old = copy.copy(toloka_client)

    pipeline_old = Pipeline()
    observer_old_1 = pipeline_old.register(AssignmentsObserver(toloka_client_old, pool_id='1'))
    observer_old_2 = pipeline_old.register(AssignmentsObserver(toloka_client_old, pool_id='2'))
    observer_old_3 = pipeline_old.register(AssignmentsObserver(toloka_client_old, pool_id='3'))
    observer_old_1.on_submitted(handler_func)
    observer_old_2.on_submitted(handler_async_func)
    observer_old_2.on_accepted(HandlerClass('w_old', 'x_old'))
    observer_old_3.on_accepted(HandlerClassCustomInject('y_old', 'z_old'))

    toloka_client_new = AsyncMultithreadWrapper(copy.copy(toloka_client))

    pipeline_new = Pipeline()
    observer_new_1 = pipeline_new.register(AssignmentsObserver(toloka_client_new, pool_id='1'))
    observer_new_2 = pipeline_new.register(AssignmentsObserver(toloka_client_new, pool_id='2'))
    observer_new_3 = pipeline_new.register(AssignmentsObserver(toloka_client_new, pool_id='3'))
    observer_new_1.on_submitted(handler_func)
    observer_new_2.on_submitted(handler_async_func)
    handler_class_new = observer_new_2.on_accepted(HandlerClass('w_new', 'x_new'))
    handler_class_custom_inject_new = observer_new_3.on_accepted(HandlerClassCustomInject('y_new', 'z_new'))

    observer_by_key_old = {observer._get_unique_key(): observer for observer in pipeline_old._observers.values()}
    for observer in pipeline_new._observers.values():
        injection = observer_by_key_old[observer._get_unique_key()]
        observer.inject(injection)

    assert 'w_old' == handler_class_new.w
    assert 'x_old' == handler_class_new.x
    assert 'y_old' == handler_class_custom_inject_new.y
    assert 'z_new' == handler_class_custom_inject_new.z
    assert observer_new_1.toloka_client.__wrapped__ is toloka_client_new


@attr.s
class HandlerToRestore:
    FAIL = True

    comment: str = attr.ib()
    saved: List = attr.ib(factory=list)
    errors: List = attr.ib(factory=list)
    iteration: int = attr.ib(default=0)

    def __call__(self, events):
        self.iteration += 1
        if self.FAIL and self.iteration > 1:
            error = ValueError(f'Test fail after: {len(self.saved)} events')
            self.errors.append(error)
            raise error
        self.saved.extend(events)


def test_save_and_load(
    requests_mock,
    toloka_url,
    toloka_client,
    existing_backend_assignments,
    new_backend_assignments,
    new_backend_assignments_after_restore,
    tmp_path,
):
    pool_mock = {'id': '100', 'status': 'OPEN'}
    pool_mock_initial = dict(pool_mock)

    backend = BackendSearchMock(existing_backend_assignments, limit=3)
    requests_mock.get(f'{toloka_url}/assignments', json=backend)
    requests_mock.get(f'{toloka_url}/pools/100', json=pool_mock)

    dirname = tmp_path / 'storage'
    dirname.mkdir()

    pipeline_old = Pipeline(storage=JSONLocalStorage(dirname=dirname), period=datetime.timedelta(milliseconds=500))
    observer_old = pipeline_old.register(AssignmentsObserver(toloka_client, pool_id='100'))
    handler_old = observer_old.on_submitted(HandlerToRestore(comment='old'))

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

    async def _main_old():
        loop = asyncio.get_event_loop()
        return await asyncio.wait(list(map(loop.create_task, (
            pipeline_old.run(),
            _add_new_assignments(after_sec=1),
            _expire_active_and_close_pool(after_sec=2),
        ))))

    res_old: Tuple[Set[asyncio.Task], Set] = asyncio.new_event_loop().run_until_complete(_main_old())

    # There should be one successfull (with initial assignments) iteration.
    # and one failed (with new assignments).

    assert 2 == handler_old.iteration
    assert 1 == len(handler_old.errors), handler_old.errors
    assert 8 == len(handler_old.saved), handler_old.saved
    assert 1 == sum(1 for task in res_old[0] if 'Test fail' in str(task.exception())), res_old

    # Now we change HandlerToRestore and allow it to finish.
    # It will be run in the similiar pipeline instance
    # and should restore from the previous success state.

    pool_mock.clear()
    pool_mock.update(pool_mock_initial)
    for item in backend.storage:
        if item['status'] == 'EXPIRED':
            item['status'] = 'ACTIVE'
    HandlerToRestore.FAIL = False

    pipeline_new = Pipeline(storage=JSONLocalStorage(dirname=dirname), period=datetime.timedelta(milliseconds=500))
    observer_new = pipeline_new.register(AssignmentsObserver(toloka_client, pool_id='100'))
    handler_new = observer_new.on_submitted(HandlerToRestore(comment='new'))

    async def _add_new_assignments_after_restore(after_sec):
        await asyncio.sleep(after_sec)
        backend.storage.extend(new_backend_assignments_after_restore)

    async def _main_new():
        loop = asyncio.get_event_loop()
        return await asyncio.wait(list(map(loop.create_task, (
            pipeline_new.run(),
            _add_new_assignments_after_restore(after_sec=1),
            _expire_active_and_close_pool(after_sec=2),
        ))))

    res_new = asyncio.new_event_loop().run_until_complete(_main_new())
    assert all(task.exception() is None for task in res_new[0]), res_new

    assert 3 == handler_new.iteration  # One successfull iteration before restore + 2 after. The errored one wasn't saved.
    assert [] == handler_new.errors, handler_new.errors  # Error attempt was not saved.
    assert 12 == len(handler_new.saved), handler_new.saved  # Start from the previous stop.


@attr.s
class HandlerToSaveAssignments:
    history = attr.ib(factory=list)
    iterations = attr.ib(default=0)

    def __call__(self, events) -> None:
        self.iterations += 1
        self.history.extend(events)


def test_async_observers():

    @attr.s
    class CountingObserver:
        history = []

        name: str = attr.ib()
        duration: float = attr.ib()
        enough_iterations: int = attr.ib()
        _count: int = attr.ib(default=0)
        _should_resume: bool = attr.ib(default=True)

        def _get_unique_key(self):
            return self.name

        async def __call__(self):
            self._count += 1
            self._should_resume = (self._count < self.enough_iterations)
            logging.info(f'Start {self.name}. Iteration: {self._count}. Sleep for: {self.duration} seconds')
            self.history.append((self.name, 'start'))
            await asyncio.sleep(self.duration)
            logging.info(f'Finish <{id(self)}>. Should resume: {self._should_resume}')
            self.history.append((self.name, 'finish'))

        async def should_resume(self):
            self.history.append((self.name, f'should_resume == {self._should_resume}'))
            return self._should_resume

    pipeline = Pipeline(period=datetime.timedelta(milliseconds=200))
    pipeline.register(CountingObserver('fast', 0.10, enough_iterations=4))
    pipeline.register(CountingObserver('slow', 0.55, enough_iterations=1))

    asyncio.new_event_loop().run_until_complete(pipeline.run())

    assert [
        ('fast', 'start'),
        ('slow', 'start'),
        ('fast', 'finish'),
        ('fast', 'should_resume == True'),
        ('fast', 'start'),
        ('fast', 'finish'),
        ('fast', 'should_resume == True'),
        ('fast', 'start'),
        ('fast', 'finish'),
        ('fast', 'should_resume == True'),
        ('slow', 'finish'),
        ('slow', 'should_resume == False'),
        ('fast', 'start'),
        ('slow', 'start'),
        ('fast', 'finish'),
        ('fast', 'should_resume == False'),
        ('slow', 'finish'),
        ('slow', 'should_resume == False'),
        ('fast', 'start'),
        ('slow', 'start'),
        ('fast', 'finish'),
        ('fast', 'should_resume == False'),
        ('slow', 'finish'),
        ('slow', 'should_resume == False')
    ] == CountingObserver.history


def test_two_pipeline_instances_run(
    requests_mock,
    toloka_url,
    toloka_client,
    existing_backend_assignments,
    new_backend_assignments,
    tmp_path,
):
    pool_mock = {'id': '100', 'status': 'OPEN'}

    backend = BackendSearchMock(existing_backend_assignments, limit=3)
    requests_mock.get(f'{toloka_url}/assignments', json=backend)
    requests_mock.get(f'{toloka_url}/pools/100', json=pool_mock)

    dirname = tmp_path / 'storage'
    dirname.mkdir()

    pipeline_1 = Pipeline(storage=JSONLocalStorage(dirname=dirname), period=datetime.timedelta(seconds=1))
    observer_1 = pipeline_1.register(AssignmentsObserver(toloka_client, pool_id='100'))
    handler_1 = observer_1.on_submitted(HandlerToSaveAssignments())

    pipeline_2 = Pipeline(storage=JSONLocalStorage(dirname=dirname), period=datetime.timedelta(seconds=1))
    observer_2 = pipeline_2.register(AssignmentsObserver(toloka_client, pool_id='100'))
    handler_2 = observer_2.on_submitted(HandlerToSaveAssignments())

    async def _run_1():
        await pipeline_1.run()

    async def _run_2(after_sec):
        await asyncio.sleep(after_sec)
        await pipeline_2.run()

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

    async def _main():
        loop = asyncio.get_event_loop()
        return await asyncio.wait(list(map(loop.create_task, (
            _run_1(),
            _run_2(after_sec=0.5),
            _add_new_assignments(after_sec=1.5),
            _expire_active_and_close_pool(after_sec=2.5),
        ))))

    done, _ = asyncio.new_event_loop().run_until_complete(_main())
    first_run_task = next(task for task in done if '_run_1' in str(task))
    assert isinstance(first_run_task.exception(), NewerInstanceDetectedError), first_run_task.exception()

    assert 1 == handler_1.iterations
    assert 8 == len(handler_1.history)

    assert 2 == handler_2.iterations
    assert 10 == len(handler_2.history)


def test_disable_observer():
    @attr.s
    class ObserverToDisableSelf(BaseObserver):
        count: int = attr.ib(default=0)

        async def should_resume(self) -> bool:
            return True

        async def __call__(self) -> None:
            self.count += 1
            self.disable()

    Pipeline.MIN_SLEEP_SECONDS = 0.01
    pipeline = Pipeline(period=datetime.timedelta(seconds=Pipeline.MIN_SLEEP_SECONDS))
    observer = pipeline.register(ObserverToDisableSelf())
    asyncio.new_event_loop().run_until_complete(pipeline.run())

    assert observer.count == 1


def test_delete_observer():
    @attr.s
    class ObserverToDeleteSelf(BaseObserver):
        count: int = attr.ib(default=0)

        async def should_resume(self) -> bool:
            return True

        async def __call__(self) -> None:
            self.count += 1
            self.delete()

    Pipeline.MIN_SLEEP_SECONDS = 0.01
    pipeline = Pipeline(period=datetime.timedelta(seconds=Pipeline.MIN_SLEEP_SECONDS))
    observer = pipeline.register(ObserverToDeleteSelf())
    assert observer in pipeline.observers_iter()

    asyncio.new_event_loop().run_until_complete(pipeline.run())

    assert observer.count == 1
    assert observer not in pipeline.observers_iter()
