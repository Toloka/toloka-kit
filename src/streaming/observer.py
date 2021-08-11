__all__ = [
    'AssignmentsObserver',
    'BaseObserver',
    'PoolStatusObserver',
]

import asyncio
import attr
import datetime
import logging

from typing import AsyncIterable, Awaitable, Callable, Dict, List, Optional, Union

from ..client import structure
from ..client.assignment import Assignment
from ..client.pool import Pool
from .cursor import AssignmentCursor, TolokaClientSyncOrAsyncType
from .event import AssignmentEvent
from .util import AsyncInterfaceWrapper, ensure_async

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


@attr.s
class BasePoolObserver(BaseObserver):

    toloka_client: TolokaClientSyncOrAsyncType = attr.ib(converter=AsyncInterfaceWrapper)
    pool_id: str = attr.ib()

    async def should_resume(self) -> bool:
        logger.debug('Check resume by pool status: %s', self.pool_id)
        pool = await self.toloka_client.get_pool(self.pool_id)
        logger.debug('Pool status for %s: %s', self.pool_id, pool.status)
        if pool.is_open():
            return True

        logger.debug('Check resume by pool active assignments: %s', self.pool_id)
        response = await self.toloka_client.find_assignments(pool_id=self.pool_id, status=[Assignment.ACTIVE], limit=1)
        logger.debug('Pool %s has active assignments: %s', self.pool_id, bool(response.items))
        return bool(response.items)


CallbackForPoolSyncType = Callable[[Pool], None]
CallbackForPoolAsyncType = Callable[[Pool], Awaitable[None]]
CallbackForPoolType = Union[CallbackForPoolSyncType, CallbackForPoolAsyncType]


@attr.s
class PoolStatusObserver(BasePoolObserver):
    """Observer for pool status change.
    For usage with Pipeline.

    Attributes:
        toloka_client: TolokaClient instance or async wrapper around it.
        pool_id: Pool ID.

    Allow to register callbacks using the following methods:
        * on_open
        * on_closed
        * on_archieved
        * on_locked
        * on_status_change

    The Pool object will be passed to the triggered callbacks.

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

    def register_callback(self, callback: CallbackForPoolType, changed_to: Union[Pool.Status, str]) -> CallbackForPoolType:
        """Register given callable for pool status change to given value.

        Args:
            callback: Sync or async callable that pass Pool object.
            changed_to: Pool status value to register for.

        Returns:
            The same callable passed as callback.
        """
        changed_to = structure(changed_to, Pool.Status)  # TODO: Autoconvert using TOLOKAKIT-83.
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
            loop = asyncio.get_event_loop()
            if self._callbacks.get(current_status):
                await asyncio.wait([
                    loop.create_task(callback(pool))
                    for callback in self._callbacks[current_status]
                ])

        self._previous_status = current_status


CallbackForAssignmentEventsSyncType = Callable[[List[AssignmentEvent]], None]
CallbackForAssignmentEventsAsyncType = Callable[[List[AssignmentEvent]], Awaitable[None]]
CallbackForAssignmentEventsType = Union[CallbackForAssignmentEventsSyncType, CallbackForAssignmentEventsAsyncType]


@attr.s
class _CursorAndCallbacks:
    cursor: AssignmentCursor = attr.ib()
    callbacks: List[CallbackForAssignmentEventsType] = attr.ib(factory=list, init=False)


@attr.s
class AssignmentsObserver(BasePoolObserver):
    """Observer for the pool's assignment events.
    For usage with Pipeline.

    Attributes:
        toloka_client: TolokaClient instance or async wrapper around it.
        pool_id: Pool ID.

    Allow to register callbacks using the following methods:
        * on_created
        * on_submitted
        * on_accepted
        * on_rejected
        * on_skipped
        * on_expired

    Corresponding assignment events will be passed to the triggered callbacks.

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

    _callbacks: Dict[AssignmentEvent.Type, _CursorAndCallbacks] = attr.ib(factory=dict, init=False)

    # Setup section.

    def register_callback(
        self,
        callback: CallbackForAssignmentEventsType,
        event_type: Union[AssignmentEvent.Type, str],
    ) -> CallbackForAssignmentEventsType:
        """Register given callable for given event type.
        Callback will be called multiple times if it has been registered for multiple event types.

        Args:
            callback: Sync or async callable that pass List[AssignmentEvent] of desired event type.
            event_type: Selected event type.

        Returns:
            The same callable passed as callback.
        """
        event_type = structure(event_type, AssignmentEvent.Type)  # TODO: Autoconvert using TOLOKAKIT-83.
        if event_type not in self._callbacks:
            cursor = AssignmentCursor(pool_id=self.pool_id, event_type=event_type, toloka_client=self.toloka_client)
            self._callbacks[event_type] = _CursorAndCallbacks(cursor)
        self._callbacks[event_type].callbacks.append(ensure_async(callback))
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

    async def _get_events(self) -> Dict[AssignmentEvent.Type, List[AssignmentEvent]]:

        async def _fetch(event_type: AssignmentEvent.Type, cursor: AsyncIterable[AssignmentEvent]):
            return event_type, [assignment async for assignment in cursor]  # TODO: Don't wait for reading all.

        return dict(await asyncio.gather(*(
            _fetch(event_type, input_to_callbacks.cursor)
            for event_type, input_to_callbacks in self._callbacks.items()
        )))

    async def __call__(self) -> None:
        if not self._callbacks:
            return

        logger.debug('Load assigment events for pool: %s', self.pool_id)
        new_events: Dict[AssignmentEvent.Type, List[AssignmentEvent]] = await self._get_events()
        logger.debug('Got assigment events count for pool %s: %d', self.pool_id, sum(map(len, new_events.values())))

        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(callback(events))
            for event_type, events in new_events.items()
            if events  # Don't run callback at empty events input.
            for callback in self._callbacks[event_type].callbacks
        ]
        if tasks:
            logger.debug('Run callbacks for assigment events in pool: %s', self.pool_id)
            await asyncio.wait(tasks)
