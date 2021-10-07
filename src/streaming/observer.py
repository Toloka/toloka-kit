__all__ = [
    'AssignmentsObserver',
    'BaseObserver',
    'PoolStatusObserver',
]

import asyncio
import attr
import datetime
import logging

from typing import Awaitable, Callable, Dict, List, Optional, Union

from ..client.primitives.base import autocast_to_enum
from ..client.assignment import Assignment
from ..client.pool import Pool
from ..util.async_utils import AsyncInterfaceWrapper, ComplexException, ensure_async, get_task_traceback
from .cursor import AssignmentCursor, TolokaClientSyncOrAsyncType
from .event import AssignmentEvent

logger = logging.getLogger(__name__)


@attr.s
class BaseObserver:
    async def __call__(self) -> None:
        raise NotImplementedError

    async def should_resume(self) -> bool:
        return False

    async def run(self, period: datetime.timedelta = datetime.timedelta(seconds=60)) -> None:
        """For standalone usage (out of a Pipeline)."""
        while True:
            await self.__call__()
            if await self.should_resume():
                logger.debug('Sleep for %d seconds', period.total_seconds())
                await asyncio.sleep(period.total_seconds())
            else:
                return


def _wrap_client_to_async_converter(client: TolokaClientSyncOrAsyncType):
    """Simple converter that is needed to specify annotation"""
    return AsyncInterfaceWrapper(client)


@attr.s
class BasePoolObserver(BaseObserver):

    toloka_client: AsyncInterfaceWrapper[TolokaClientSyncOrAsyncType] = attr.ib(converter=_wrap_client_to_async_converter)
    pool_id: str = attr.ib()

    async def should_resume(self) -> bool:
        logger.info('Check resume by pool status: %s', self.pool_id)
        pool = await self.toloka_client.get_pool(self.pool_id)
        logger.info('Pool status for %s: %s', self.pool_id, pool.status)
        if pool.is_open():
            return True

        logger.info('Check resume by pool active assignments: %s', self.pool_id)
        response = await self.toloka_client.find_assignments(pool_id=self.pool_id, status=[Assignment.ACTIVE], limit=1)
        logger.info('Pool %s has active assignments: %s', self.pool_id, bool(response.items))
        return bool(response.items)


CallbackForPoolSyncType = Callable[[Pool], None]
CallbackForPoolAsyncType = Callable[[Pool], Awaitable[None]]
CallbackForPoolType = Union[CallbackForPoolSyncType, CallbackForPoolAsyncType]


@attr.s
class PoolStatusObserver(BasePoolObserver):
    """Observer for pool status change.
    For usage with Pipeline.

    Allow to register callbacks using the following methods:
        * on_open
        * on_closed
        * on_archieved
        * on_locked
        * on_status_change

    The Pool object will be passed to the triggered callbacks.

    Attributes:
        toloka_client: TolokaClient instance or async wrapper around it.
        pool_id: Pool ID.

    Examples:
        Bind to the pool's close to make some aggregations.

        >>> def call_this_on_close(pool: Pool) -> None:
        >>>     assignments = client.get_assignments_df(pool_id=pool.id, status=['APPROVED'])
        >>>     do_some_aggregation(assignments)
        >>>
        >>> observer = PoolStatusObserver(toloka_client, pool_id='123')
        >>> observer.on_close(call_this_on_close)
        ...

        Call something at any status change.

        >>> observer.on_status_change(lambda pool: ...)
        ...
    """

    _callbacks: Dict[Pool.Status, List[CallbackForPoolAsyncType]] = attr.ib(factory=dict, init=False)
    _previous_status: Optional[Pool.Status] = attr.ib(default=None, init=False)

    @autocast_to_enum
    def register_callback(
        self,
        callback: CallbackForPoolType,
        changed_to: Pool.Status
    ) -> CallbackForPoolType:
        """Register given callable for pool status change to given value.

        Args:
            callback: Sync or async callable that pass Pool object.
            changed_to: Pool status value to register for.

        Returns:
            The same callable passed as callback.
        """

        self._callbacks.setdefault(changed_to, []).append(ensure_async(callback))
        return callback

    def on_open(self, callback: CallbackForPoolType) -> CallbackForPoolType:
        return self.register_callback(callback, Pool.Status.OPEN)

    def on_closed(self, callback: CallbackForPoolType) -> CallbackForPoolType:
        return self.register_callback(callback, Pool.Status.CLOSED)

    def on_archieved(self, callback: CallbackForPoolType) -> CallbackForPoolType:
        return self.register_callback(callback, Pool.Status.ARCHIEVED)

    def on_locked(self, callback: CallbackForPoolType) -> CallbackForPoolType:
        return self.register_callback(callback, Pool.Status.LOCKED)

    def on_status_change(self, callback: CallbackForPoolType) -> CallbackForPoolType:
        for status in Pool.Status.__members__:
            self.register_callback(callback, status)
        return callback

    async def __call__(self) -> None:
        if not self._callbacks:
            return

        pool = await self.toloka_client.get_pool(self.pool_id)
        current_status = pool.status

        if current_status != self._previous_status:
            logger.info('Pool %s status change: %s -> %s', self.pool_id, self._previous_status, current_status)
            if self._callbacks.get(current_status):
                loop = asyncio.get_event_loop()
                done, _ = await asyncio.wait([loop.create_task(callback(pool))
                                              for callback in self._callbacks[current_status]])
                errored = [task for task in done if task.exception() is not None]
                if errored:
                    for task in errored:
                        logger.error('Got error while handling pool %s status change to: %s\n%s',
                                     self.pool_id, current_status, get_task_traceback(task))
                    raise ComplexException([task.exception() for task in errored])

        self._previous_status = current_status


CallbackForAssignmentEventsSyncType = Callable[[List[AssignmentEvent]], None]
CallbackForAssignmentEventsAsyncType = Callable[[List[AssignmentEvent]], Awaitable[None]]
CallbackForAssignmentEventsType = Union[CallbackForAssignmentEventsSyncType, CallbackForAssignmentEventsAsyncType]


@attr.s
class _CallbacksCursorConsumer:
    """Store cursor and related callbacks.
    Allow to run callbacks at fetched data and move the cursor in case of success.
    """
    cursor: AssignmentCursor = attr.ib()
    callbacks: List[CallbackForAssignmentEventsAsyncType] = attr.ib(factory=list, init=False)

    def add_callback(self, callback: CallbackForAssignmentEventsType) -> None:
        self.callbacks.append(ensure_async(callback))

    async def __call__(self, pool_id: str) -> None:
        async with self.cursor.try_fetch_all() as fetched:
            if not fetched:
                return

            logger.info('Got pool %s events count of type %s: %d', pool_id, fetched[0].event_type, len(fetched))
            loop = asyncio.get_event_loop()
            callback_by_task = {loop.create_task(callback(fetched)): callback
                                for callback in self.callbacks}
            done, _ = await asyncio.wait(callback_by_task)
            errored = [task for task in done if task.exception() is not None]
            if errored:
                for task in errored:
                    logger.error('Got error in callback: %s\n%s', callback_by_task[task], get_task_traceback(task))
                raise ComplexException([task.exception() for task in errored])


@attr.s
class AssignmentsObserver(BasePoolObserver):
    """Observer for the pool's assignment events.
    For usage with Pipeline.

    Allow to register callbacks using the following methods:
        * on_created
        * on_submitted
        * on_accepted
        * on_rejected
        * on_skipped
        * on_expired

    Corresponding assignment events will be passed to the triggered callbacks.

    Attributes:
        toloka_client: TolokaClient instance or async wrapper around it.
        pool_id: Pool ID.

    Examples:
        Send submitted assignments for verification.

        >>> def handle_submitted(evets: List[AssignmentEvent]) -> None:
        >>>     verification_tasks = [create_veridication_task(item.assignment) for item in evets]
        >>>     toloka_client.create_tasks(verification_tasks, open_pool=True)
        >>>
        >>> observer = AssignmentsObserver(toloka_client, pool_id='123')
        >>> observer.on_submitted(handle_submitted)
        ...
    """

    _callbacks: Dict[AssignmentEvent.Type, _CallbacksCursorConsumer] = attr.ib(factory=dict, init=False)

    # Setup section.

    @autocast_to_enum
    def register_callback(
        self,
        callback: CallbackForAssignmentEventsType,
        event_type: AssignmentEvent.Type,
    ) -> CallbackForAssignmentEventsType:
        """Register given callable for given event type.
        Callback will be called multiple times if it has been registered for multiple event types.

        Args:
            callback: Sync or async callable that pass List[AssignmentEvent] of desired event type.
            event_type: Selected event type.

        Returns:
            The same callable passed as callback.
        """
        if event_type not in self._callbacks:
            cursor = AssignmentCursor(pool_id=self.pool_id, event_type=event_type, toloka_client=self.toloka_client)
            self._callbacks[event_type] = _CallbacksCursorConsumer(cursor)
        self._callbacks[event_type].add_callback(callback)
        return callback

    def on_any_event(self, callback: CallbackForAssignmentEventsType) -> CallbackForAssignmentEventsType:
        for event_type in AssignmentEvent.Type.__members__.values():
            self.register_callback(callback, event_type)
        return callback

    def on_created(self, callback: CallbackForAssignmentEventsType) -> CallbackForAssignmentEventsType:
        return self.register_callback(callback, AssignmentEvent.Type.CREATED)

    def on_submitted(self, callback: CallbackForAssignmentEventsType) -> CallbackForAssignmentEventsType:
        return self.register_callback(callback, AssignmentEvent.Type.SUBMITTED)

    def on_accepted(self, callback: CallbackForAssignmentEventsType) -> CallbackForAssignmentEventsType:
        return self.register_callback(callback, AssignmentEvent.Type.ACCEPTED)

    def on_rejected(self, callback: CallbackForAssignmentEventsType) -> CallbackForAssignmentEventsType:
        return self.register_callback(callback, AssignmentEvent.Type.REJECTED)

    def on_skipped(self, callback: CallbackForAssignmentEventsType) -> CallbackForAssignmentEventsType:
        return self.register_callback(callback, AssignmentEvent.Type.SKIPPED)

    def on_expired(self, callback: CallbackForAssignmentEventsType) -> CallbackForAssignmentEventsType:
        return self.register_callback(callback, AssignmentEvent.Type.EXPIRED)

    # Run section.

    async def __call__(self) -> None:
        if not self._callbacks:
            return

        loop = asyncio.get_event_loop()
        event_type_by_task = {loop.create_task(cursor_and_callbacks(self.pool_id)): event_type
                              for event_type, cursor_and_callbacks in self._callbacks.items()
                              if cursor_and_callbacks.callbacks}
        logger.info('Gathering pool %s event of types: %s', self.pool_id, list(event_type_by_task.values()))

        done, _ = await asyncio.wait(event_type_by_task)
        errored = [task for task in done if task.exception() is not None]
        if errored:
            for task in errored:
                logger.error('Got error while handling pool %s assignment events of type: %s',
                             self.pool_id, event_type_by_task[task])
            raise ComplexException([task.exception() for task in errored])
