__all__ = [
    'Pipeline',
]

import asyncio
import attr
import itertools
import logging
import signal

from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Container, ContextManager, Dict, Iterable, Iterator, List, Optional, Set, Tuple

from .observer import BaseObserver
from .storage import BaseStorage
from ..util.async_utils import ComplexException
from ..util._managing_headers import async_add_headers

logger = logging.getLogger(__name__)


_OrderedSet = dict.fromkeys


@attr.s(eq=False, hash=False)
class _Worker:
    """_Worker object that run observer's __call__() and should_resume() methods.
    Keep track of the observer's should_resume state.

    Attributes:
        name: Unique key to be identified by.
        observer: BaseObserver object to run.
        should_resume: Current observer's should_resume state.
    """
    name: str = attr.ib()
    observer: BaseObserver = attr.ib()
    should_resume: bool = attr.ib(default=False)

    @async_add_headers('streaming')
    async def __call__(self) -> None:
        if getattr(self.observer, '_enabled', True):
            await self.observer()
            self.should_resume = await self.observer.should_resume()
        else:
            self.should_resume = False

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: '_Worker') -> bool:
        return self.name == other.name

    @classmethod
    def _from_observer(cls, observer: BaseObserver) -> '_Worker':
        return cls(str(observer._get_unique_key()), observer)

    @staticmethod
    def _no_one_should_resume(workers: Iterable['_Worker']) -> bool:
        return all(not worker.should_resume for worker in workers)

    def _is_deleted(self) -> bool:
        return getattr(self.observer, '_deleted', False)


@attr.s
class Pipeline:
    """An entry point for toloka streaming pipelines.
    Allow you to register multiple observers and call them periodically
    while at least one of them may resume.

    Attributes:
        period: Period of observers calls. By default, 60 seconds.
        storage: Optional storage object to save pipeline's state.
            Allow to recover from previous state in case of failure.

    Examples:
        Get assignments from segmentation pool and send them for verification to another pool.

        >>> def handle_submitted(events: List[AssignmentEvent]) -> None:
        >>>     verification_tasks = [create_verification_task(item.assignment) for item in events]
        >>>     toloka_client.create_tasks(verification_tasks, open_pool=True)
        >>>
        >>> def handle_accepted(events: List[AssignmentEvent]) -> None:
        >>>     do_some_aggregation([item.assignment for item in events])
        >>>
        >>> async_toloka_client = AsyncMultithreadWrapper(toloka_client)
        >>>
        >>> observer_123 = AssignmentsObserver(async_toloka_client, pool_id='123')
        >>> observer_123.on_submitted(handle_submitted)
        >>>
        >>> observer_456 = AssignmentsObserver(async_toloka_client, pool_id='456')
        >>> observer_456.on_accepted(handle_accepted)
        >>>
        >>> pipeline = Pipeline()
        >>> pipeline.register(observer_123)
        >>> pipeline.register(observer_456)
        >>> await pipeline.run()
        ...

        One-liners version.

        >>> pipeline = Pipeline()
        >>> pipeline.register(AssignmentsObserver(toloka_client, pool_id='123')).on_submitted(handle_submitted)
        >>> pipeline.register(AssignmentsObserver(toloka_client, pool_id='456')).on_accepted(handle_accepted)
        >>> await pipeline.run()
        ...

        With external storage.

        >>> from toloka.streaming import S3Storage, ZooKeeperLocker
        >>> locker = ZooKeeperLocker(...)
        >>> storage = S3Storage(locker=locker, ...)
        >>> pipeline = Pipeline(storage=storage)
        >>> await pipeline.run()  # Save state after each iteration. Try to load saved at start.
        ...
    """

    MIN_SLEEP_SECONDS = 10  # Allow lock to be taken in concurrent cases.

    period: timedelta = attr.ib(default=timedelta(seconds=60))
    storage: Optional[BaseStorage] = attr.ib(default=None)
    name: Optional[str] = attr.ib(default=None, kw_only=True)
    _observers: Dict[int, BaseObserver] = attr.ib(factory=dict, init=False)
    _got_sigint: bool = attr.ib(default=False, init=False)

    @contextmanager
    def _lock(self, key: str) -> ContextManager[Any]:
        if self.storage:
            with self.storage.lock(key) as lock:
                yield lock
                return
        yield None

    def _storage_load(self, pipeline_key: str, workers: Iterable[_Worker]) -> None:
        if self.storage:
            logger.info('Loading state from storage: %s', type(self.storage).__name__)
            observer_by_key = {worker.name: worker.observer for worker in workers}
            state_by_key = self.storage.load(pipeline_key, observer_by_key.keys())
            if state_by_key:
                logger.info('Found saved states count: %d / %d', len(state_by_key), len(observer_by_key))
                for key, injection in state_by_key.items():
                    observer_by_key[key].inject(injection)
            else:
                logger.info('No saved states found')

    def _storage_save(self, pipeline_key: str, workers: Iterable[_Worker]) -> None:
        if self.storage:
            logger.info('Save state to: %s', type(self.storage).__name__)
            observer_by_key = {worker.name: worker.observer for worker in workers}
            self.storage.save(pipeline_key, observer_by_key)
            logger.info('Saved count: %d', len(observer_by_key))

    def _storage_cleanup(self, pipeline_key: str, workers: Iterable[_Worker], lock: Any) -> None:
        if self.storage:
            try:
                keys = {worker.name for worker in workers}
                logger.info('Cleanup storage %s with keys count: %d', type(self.storage).__name__, len(keys))
                self.storage.cleanup(pipeline_key, keys, lock)
            except Exception:
                logger.exception('Got an exception while running cleanup at: %s', type(self.storage).__name__)

    def _get_unique_key(self) -> Tuple:
        return (self.__class__.__name__, self.name or '', tuple(sorted(
            observer._get_unique_key()
            for observer in self._observers.values()
        )))

    def register(self, observer: BaseObserver) -> BaseObserver:
        """Register given observer.

        Args:
            observer: Observer object.

        Returns:
            The same observer object. It's usable to write one-liners.

        Examples:
            Register observer.

            >>> observer = SomeObserver(pool_id='123')
            >>> observer.do_some_preparations(...)
            >>> toloka_loop.register(observer)
            ...

            One-line version.

            >>> toloka_loop.register(SomeObserver(pool_id='123')).do_some_preparations(...)
            ...
        """
        self._observers[id(observer)] = observer
        return observer

    def observers_iter(self) -> Iterator[BaseObserver]:
        """Iterate over registered observers.

        Returns:
            An iterator over all registered observers except deleted ones.
            Might contain observers scheduled for deletion and not deleted yet.
        """
        return iter(self._observers.values())

    def _sigint_handler(self, loop: asyncio.AbstractEventLoop, waiting: Container[_Worker]) -> None:
        """Is being called in case of KeyboardInterrupt during workers run."""
        logger.error('Gracefully shutdown...')
        loop.remove_signal_handler(signal.SIGINT)
        self._got_sigint = True
        if not waiting:
            logger.warning('No workers to wait')
            raise KeyboardInterrupt

    def _process_done_tasks(
        self,
        pipeline_key: str,
        done: Set[asyncio.Task],
        waiting: Dict[_Worker, asyncio.Task],
        pending: Dict[_Worker, datetime],
    ) -> None:
        """Take done tasks and modify `waiting` and `pending`."""
        logger.info('Done count: %d', len(done))
        workers_to_dump = []
        errored = []
        for task in done:
            del waiting[task.worker]
            if task.exception():
                errored.append(task)
            else:
                workers_to_dump.append(task.worker)
                pending[task.worker] = task.start_time + self.period
        self._storage_save(pipeline_key, workers_to_dump)
        if errored:
            asyncio.get_event_loop().remove_signal_handler(signal.SIGINT)
            for task in errored:
                logger.error('Got error in: %s', task)
            raise ComplexException([task.exception() for task in errored])

    async def run(self) -> None:
        if not self._observers:
            raise ValueError('No observers registered')
        self._got_sigint = False

        pipeline_key: str = str(self._get_unique_key())

        workers = _OrderedSet(())
        waiting: Dict[_Worker, asyncio.Task] = {}
        pending: Dict[_Worker, datetime] = {}

        def _add_new_observers(new_observers: Iterable[BaseObserver]) -> None:
            new_workers = _OrderedSet(_Worker._from_observer(observer) for observer in new_observers)
            workers.update(new_workers)
            pending.update({worker: datetime.min for worker in new_workers})

        _add_new_observers(self.observers_iter())

        check_mode = False

        for iteration in itertools.count(1):
            logger.info('Iteration %d', iteration)

            with self._lock(pipeline_key) as lock:
                if iteration == 1:  # Get checkpoint from the storage.
                    self._storage_load(pipeline_key, workers)
                    loop = asyncio.get_event_loop()
                    loop.add_signal_handler(signal.SIGINT, self._sigint_handler, loop, waiting)

                iteration_start = datetime.now()

                still_pending = {}
                to_start: List[_Worker] = []
                to_remove: List[_Worker] = []
                for worker, time_to_start in pending.items():
                    if worker._is_deleted():
                        to_remove.append(worker)
                    elif time_to_start <= iteration_start or check_mode:
                        assert worker not in waiting
                        to_start.append(worker)
                    else:
                        still_pending[worker] = time_to_start
                pending = still_pending

                if to_remove:
                    logger.info('Found observers to remove count: %d', len(to_remove))
                    for worker in to_remove:
                        self._observers.pop(id(worker.observer))
                        workers.pop(worker)

                if self._got_sigint:
                    logger.warning('Not starting new workers due to SIGINT received')
                    to_start = []
                else:
                    logger.info('Observers to run count: %d', len(to_start))
                    for worker in to_start:
                        task = asyncio.get_event_loop().create_task(worker())
                        task.worker = worker
                        task.start_time = iteration_start
                        waiting[worker] = task

                return_when = asyncio.FIRST_COMPLETED
                if check_mode:
                    return_when = asyncio.ALL_COMPLETED
                    logger.info('Check resume all')
                if self._got_sigint:
                    return_when = asyncio.ALL_COMPLETED
                    logger.warning('Need to wait all working')

                if waiting:  # It may be empty due to SIGINT.
                    done, _ = await asyncio.wait(waiting.values(), return_when=return_when)
                    self._process_done_tasks(pipeline_key, done, waiting, pending)
                elif self._got_sigint:
                    raise KeyboardInterrupt
                else:
                    logger.info('No workers to process. Finish')
                    return

                if _Worker._no_one_should_resume(workers):  # But some of them may still work.
                    if check_mode:
                        self._storage_cleanup(pipeline_key, workers, lock)
                        logger.info('Finish')
                        asyncio.get_event_loop().remove_signal_handler(signal.SIGINT)
                        return

                    logger.info('No one should resume yet. Waiting for remaining ones...')
                    if waiting:
                        done, _ = await asyncio.wait(waiting.values(), return_when=asyncio.ALL_COMPLETED)
                    else:
                        done = set()
                    self._process_done_tasks(pipeline_key, done, waiting, pending)
                    if self._got_sigint:
                        raise KeyboardInterrupt
                    if _Worker._no_one_should_resume(workers):  # If stop condition at all workers, run in check_mode.
                        check_mode = True
                    start_soon = max(pending.values(), default=None)
                else:
                    check_mode = False
                    start_soon = min(pending.values(), default=None)

            if self._got_sigint:
                logger.warning('No sleeping while SIGINT handling')
            else:
                sleep_time = (start_soon - datetime.now()).total_seconds()
                sleep_time = max(sleep_time, self.MIN_SLEEP_SECONDS)

                logger.info('Sleeping for %f seconds', sleep_time)
                await asyncio.sleep(sleep_time)

            new_observers_ids = self._observers.keys() - {id(worker.observer) for worker in workers}
            if new_observers_ids:
                logger.info('New observers found in quantity: %d', len(new_observers_ids))
                new_observers = (self._observers[id_] for id_ in new_observers_ids)
                _add_new_observers(new_observers)
