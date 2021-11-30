__all__ = [
    'Pipeline',
]

import asyncio
import attr
import datetime
import itertools
import logging

from contextlib import contextmanager
from typing import Any, ContextManager, Dict, List, Optional, Tuple

from .observer import BaseObserver
from .storage import BaseStorage
from ..util.async_utils import ComplexException

logger = logging.getLogger(__name__)


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

    period: datetime.timedelta = attr.ib(default=datetime.timedelta(seconds=60))
    storage: Optional[BaseStorage] = attr.ib(default=None)
    name: Optional[str] = attr.ib(default=None, kw_only=True)
    _observers: Dict[int, BaseObserver] = attr.ib(factory=dict, init=False)

    @contextmanager
    def _lock(self, key: str) -> ContextManager[Any]:
        if self.storage:
            with self.storage.lock(key) as lock:
                yield lock
                return
        yield None

    def _storage_load(self, key: str) -> None:
        if self.storage:
            logger.info('Loading state from %s by key: %s', type(self.storage).__name__, key)
            state: Optional[Pipeline] = self.storage.load(key)
            if state:
                logger.info('State loaded')
                self.inject(state)
            else:
                logger.info('State not found')

    def _storage_save(self, key: str) -> None:
        if self.storage:
            logger.info('Save state to %s by key: %s', type(self.storage).__name__, key)
            self.storage.save(key, self)
            logger.info('State saved')

    def _cleanup_storage(self, key: str, lock: Any) -> None:
        if self.storage:
            try:
                logger.info('Cleanup storage %s by key: %s', type(self.storage).__name__, key)
                self.storage.cleanup(key, lock)
            except Exception:
                logger.exception('Got exception while running cleanup at %s', type(self.storage).__name__)

    def _get_unique_key(self) -> Tuple:
        return (self.__class__.__name__, self.name or '', tuple(sorted(
            observer._get_unique_key()
            for observer in self._observers.values()
        )))

    def inject(self, injection: 'Pipeline') -> None:
        injection_by_key = {
            observer._get_unique_key(): observer
            for observer in injection._observers.values()
        }
        for observer in self._observers.values():
            key = observer._get_unique_key()
            observer.inject(injection_by_key[key])

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

    async def run(self):
        if not self._observers:
            raise ValueError('No observers registered')

        key: str = str(self._get_unique_key())

        for iteration in itertools.count(1):
            logger.info('Iteration: %d', iteration)

            with self._lock(key) as lock:
                if iteration == 1:  # Get checkpoint from the storage.
                    self._storage_load(key)

                logger.info('Run observers count: %d', len(self._observers))
                loop = asyncio.get_event_loop()
                done, _ = await asyncio.wait([loop.create_task(observer()) for observer in self._observers.values()])
                errored = [task for task in done if task.exception() is not None]
                if errored:
                    for task in errored:
                        logger.error('Got error in: %s', task)
                    # TODO: Also save state here except errored entities.
                    raise ComplexException([task.exception() for task in errored])

                logger.info('Check resume')
                may_resume_each: List[bool] = await asyncio.gather(*[
                    observer.should_resume()
                    for observer in self._observers.values()
                    if getattr(observer, 'should_resume', None)
                ])

                self._storage_save(key)

                if all(not resume for resume in may_resume_each):
                    self._cleanup_storage(key, lock)
                    logger.info('Finish')
                    return

            logger.info('Sleep for %d seconds', self.period.total_seconds())
            await asyncio.sleep(self.period.total_seconds())
