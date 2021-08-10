__all__ = [
    'AssignmentCursor',
    'BaseCursor',
    'DATETIME_MIN',
    'TaskCursor',
    'TolokaClientSyncOrAsyncType',
    'UserBonusCursor',
    'UserSkillCursor',
]

import attr
import functools
import logging
from datetime import datetime
from typing import Any, AsyncIterator, Callable, Iterator, Optional, TypeVar, Union

from ..client import (
    Assignment,
    Task,
    TolokaClient,
    UserBonus,
    UserSkill,
    expand,
    search_requests,
    search_results,
    structure,
)
from .event import AssignmentEvent, BaseEvent, TaskEvent, UserBonusEvent, UserSkillEvent
from .util import AsyncMultithreadWrapper, ensure_async


RequestObjectType = TypeVar('RequestObjectType')
ResponseObjectType = TypeVar('ResponseObjectType')
TolokaClientSyncOrAsyncType = Union[TolokaClient, AsyncMultithreadWrapper[TolokaClient]]

DATETIME_MIN = datetime.fromtimestamp(0)


logger = logging.getLogger(__name__)


@attr.s
class _ByIdCursor:
    """Iterate by id only."""
    fetcher: Callable[[RequestObjectType], ResponseObjectType] = attr.ib()
    request: RequestObjectType = attr.ib()

    def __iter__(self) -> Iterator[Any]:
        while True:
            response = self.fetcher(self.request, sort='id')  # Diff between sync and async.
            if response.items:
                for item in response.items:
                    yield item
                self.request = attr.evolve(self.request, id_gt=item.id)
            if not response.has_more:
                return

    async def __aiter__(self) -> AsyncIterator[Any]:
        while True:
            response = await ensure_async(self.fetcher)(self.request, sort='id')  # Diff between sync and async.
            if response.items:
                for item in response.items:
                    yield item
                self.request = attr.evolve(self.request, id_gt=item.id)
            if not response.has_more:
                return


@attr.s
class BaseCursor:
    toloka_client: TolokaClientSyncOrAsyncType = attr.ib()
    _request: RequestObjectType = attr.ib()
    _prev_response: Optional[ResponseObjectType] = attr.ib(default=None, init=False)

    def __attrs_post_init__(self):
        if not getattr(self._request, self._time_field_gte):
            self._request = attr.evolve(self._request, **{self._time_field_gte: DATETIME_MIN})

    def _get_fetcher(self) -> Callable[..., ResponseObjectType]:
        """Return toloka_client method from here."""
        raise NotImplementedError

    def _get_time_field(self) -> str:
        """Getter for time field."""
        raise NotImplementedError

    def _construct_event(self, item: Any) -> BaseEvent:
        """Create event based on object."""
        raise NotImplementedError

    def _get_time(self, item: Any) -> datetime:
        return getattr(item, self._get_time_field())

    @property
    def _time_field_gte(self) -> str:
        return f'{self._get_time_field()}_gte'

    @property
    def _time_field_lte(self) -> str:
        return f'{self._get_time_field()}_lte'  # To iterate by id for fixed time.

    @property
    def _time_field_gt(self) -> str:
        return f'{self._get_time_field()}_gt'  # To use after iteration by id.

    def __iter__(self) -> Iterator[BaseEvent]:
        fetcher = self._get_fetcher()
        while True:
            response = fetcher(self._request, sort=self._get_time_field())  # Diff between sync and async.
            if response.items:
                max_time = self._get_time(response.items[-1])
                self._request = attr.evolve(self._request, **{self._time_field_gte: max_time})
                seen_ids = frozenset(item.id for item in self._prev_response.items) if self._prev_response else ()
                for item in response.items:
                    if item.id not in seen_ids:
                        yield self._construct_event(item)

                self._prev_response = response
                if not response.has_more:
                    return

                if self._get_time(response.items[0]) == max_time:
                    fixed_time_request = attr.evolve(self._request, **{self._time_field_lte: max_time})
                    seen_ids = frozenset(item.id for item in response.items)
                    for item in _ByIdCursor(fetcher, fixed_time_request):  # Diff between sync and async.
                        if item.id not in seen_ids:
                            yield self._construct_event(item)
                    self._request = attr.evolve(self._request, **{self._time_field_gt: max_time})
            else:
                return

    async def __aiter__(self) -> AsyncIterator[BaseEvent]:
        fetcher = self._get_fetcher()
        while True:
            response = await ensure_async(fetcher)(self._request, sort=self._get_time_field())  # Diff between sync and async.
            if response.items:
                max_time = self._get_time(response.items[-1])
                self._request = attr.evolve(self._request, **{self._time_field_gte: max_time})
                seen_ids = frozenset(item.id for item in self._prev_response.items) if self._prev_response else ()
                for item in response.items:
                    if item.id not in seen_ids:
                        yield self._construct_event(item)

                self._prev_response = response
                if not response.has_more:
                    return

                if self._get_time(response.items[0]) == max_time:
                    fixed_time_request = attr.evolve(self._request, **{self._time_field_lte: max_time})
                    seen_ids = frozenset(item.id for item in response.items)
                    async for item in _ByIdCursor(fetcher, fixed_time_request):  # Diff between sync and async.
                        if item.id not in seen_ids:
                            yield self._construct_event(item)
                    self._request = attr.evolve(self._request, **{self._time_field_gt: max_time})
            else:
                return


@expand('request')
@attr.s
class AssignmentCursor(BaseCursor):
    """Iterator over Assignment objects of seleted AssignmentEventType.

    Args:
        toloka_client: TolokaClient object that is being used to search assignments.
        request: Base request to search assignments by.
        event_type: Assignments event's type to search.

    Examples:
        Iterate over assignment acceptances events.

        >>> it = AssignmentCursor(pool_id='123', event_type='ACCEPTED', toloka_client=toloka_client)
        >>> current_events = list(it)
        >>> # ... new events may occur ...
        >>> new_events = list(it)  # Contains only new events, occured since the previous call.
        ...
    """

    _event_type: AssignmentEvent.Type = attr.ib(converter=functools.partial(structure, cl=AssignmentEvent.Type))
    _request: search_requests.AssignmentSearchRequest = attr.ib(
        converter=search_requests.AssignmentSearchRequest.structure,
        factory=search_requests.AssignmentSearchRequest,
    )

    def _get_fetcher(self) -> Callable[..., search_results.AssignmentSearchResult]:
        return self.toloka_client.find_assignments

    def _get_time_field(self) -> str:
        return self._event_type.time_key

    def _construct_event(self, item: Assignment) -> AssignmentEvent:
        return AssignmentEvent(assignment=item,
                               event_type=self._event_type,
                               event_time=getattr(item, self._event_type.time_key))


@expand('request')
@attr.s
class TaskCursor(BaseCursor):
    """Iterator over tasks by create time.

    Args:
        toloka_client: TolokaClient object that is being used to search tasks.
        request: Base request to search tasks by.

    Examples:
        Iterate over tasks.

        >>> it = TaskCursor(pool_id='123', toloka_client=toloka_client)
        >>> current_tasks = list(it)
        >>> # ... new tasks could appear ...
        >>> new_tasks = list(it)  # Contains only new tasks, appeared since the previous call.
        ...
    """

    _request: search_requests.TaskSearchRequest = attr.ib(
        converter=search_requests.TaskSearchRequest.structure,
        factory=search_requests.TaskSearchRequest,
    )

    def _get_fetcher(self) -> Callable[..., search_results.TaskSearchResult]:
        return self.toloka_client.find_tasks

    def _get_time_field(self) -> str:
        return 'created'

    def _construct_event(self, item: Task) -> TaskEvent:
        return TaskEvent(task=item, event_time=item.created)


@expand('request')
@attr.s
class UserBonusCursor(BaseCursor):
    """Iterator over user bonuses by create time.

    Args:
        toloka_client: TolokaClient object that is being used to search user bonuses.
        request: Base request to search user bonuses by.

    Examples:
        Iterate over user bonuses.

        >>> it = UserBonusCursortoloka_client=toloka_client)
        >>> current_bonuses = list(it)
        >>> # ... new user bonuses could appear ...
        >>> new_bonuses = list(it)  # Contains only new user bonuses, appeared since the previous call.
        ...
    """

    _request: search_requests.UserBonusSearchRequest = attr.ib(
        converter=search_requests.UserBonusSearchRequest.structure,
        factory=search_requests.UserBonusSearchRequest,
    )

    def _get_fetcher(self) -> Callable[..., search_results.UserBonusSearchResult]:
        return self.toloka_client.find_user_bonuses

    def _get_time_field(self) -> str:
        return 'created'

    def _construct_event(self, item: UserBonus) -> UserBonusEvent:
        return UserBonusEvent(user_bonus=item, event_time=item.created)


@expand('request')
@attr.s
class UserSkillCursor(BaseCursor):
    """Iterator over UserSkillEvent objects of seleted event_type.

    Args:
        toloka_client: TolokaClient object that is being used to search user skills.
        request: Base request to search user skills by.
        event_type: User skill event's type to search.

    Examples:
        Iterate over user skills acceptances events.

        >>> it = UserSkillCursorevent_type='MODIFIED', toloka_client=toloka_client)
        >>> current_events = list(it)
        >>> # ... new user skills could be set ...
        >>> new_events = list(it)  # Contains only new events, occured since the previous call.
        ...
    """

    _event_type: UserSkillEvent.Type = attr.ib(converter=functools.partial(structure, cl=UserSkillEvent.Type))
    _request: search_requests.UserSkillSearchRequest = attr.ib(
        converter=search_requests.UserSkillSearchRequest.structure,
        factory=search_requests.UserSkillSearchRequest,
    )

    def _get_fetcher(self) -> Callable[..., search_results.UserSkillSearchResult]:
        return self.toloka_client.find_user_skills

    def _get_time_field(self) -> str:
        return self._event_type.time_key

    def _construct_event(self, item: UserSkill) -> UserSkillEvent:
        return UserSkillEvent(user_skill=item,
                              event_type=self._event_type,
                              event_time=getattr(item, self._event_type.time_key))
