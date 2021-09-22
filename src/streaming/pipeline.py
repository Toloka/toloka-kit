__all__ = [
    'Pipeline',
]

import asyncio
import attr
import datetime
import itertools
import logging

from typing import Dict, List

from .observer import BaseObserver
from ..util.async_utils import ComplexException

logger = logging.getLogger(__name__)


@attr.s
class Pipeline:
    """An entry point for toloka streaming pipelines.
    Allow you to register multiple observers and call them periodically
    while at least one of them may resume.

    Attributes:
        period: Period of observers calls. By default, 60 seconds.

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
    """

    period: datetime.timedelta = attr.ib(default=datetime.timedelta(seconds=60))
    _observers: Dict[int, BaseObserver] = attr.ib(factory=dict, init=False)

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

        for iteration in itertools.count(1):
            logger.debug('Iteration: %d', iteration)
            logger.debug('Run observers count: %d', len(self._observers))
            loop = asyncio.get_event_loop()
            done, _ = await asyncio.wait([loop.create_task(observer()) for observer in self._observers.values()])
            errored = [task for task in done if task.exception() is not None]
            if errored:
                for task in errored:
                    logger.error('Got error in: %s', task)
                raise ComplexException([task.exception() for task in errored])

            logger.debug('Check resume')
            may_resume_each: List[bool] = await asyncio.gather(*[
                observer.should_resume()
                for observer in self._observers.values()
                if getattr(observer, 'should_resume', None)
            ])
            if any(may_resume_each):
                logger.debug('Sleep for %d seconds', self.period.total_seconds())
                await asyncio.sleep(self.period.total_seconds())
            else:
                logger.debug('Finish')
                return
