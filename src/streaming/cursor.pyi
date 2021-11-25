__all__ = [
    'AssignmentCursor',
    'BaseCursor',
    'DATETIME_MIN',
    'MessageThreadCursor',
    'TaskCursor',
    'TolokaClientSyncOrAsyncType',
    'UserBonusCursor',
    'UserRestrictionCursor',
    'UserSkillCursor',
]
import datetime
import toloka.client
import toloka.client.assignment
import toloka.client.message_thread
import toloka.client.search_requests
import toloka.client.user_restriction
import toloka.streaming.event
import toloka.util.async_utils
import typing


RequestObjectType = typing.TypeVar('RequestObjectType')

ResponseObjectType = typing.TypeVar('ResponseObjectType')

TolokaClientSyncOrAsyncType = typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]]


DATETIME_MIN = ...

class BaseCursor:
    class CursorFetchContext:
        """Context manager to return from `BaseCursor.try_fetch_all method`.
        Commit cursor state only if no error occured.
        """

        def __init__(self, cursor: 'BaseCursor') -> None:
            """Method generated by attrs for class BaseCursor.CursorFetchContext.
            """
            ...

        _cursor: 'BaseCursor'
        _start_state: typing.Optional[typing.Tuple]
        _finish_state: typing.Optional[typing.Tuple]

    def inject(self, injection: 'BaseCursor') -> None: ...

    def try_fetch_all(self) -> CursorFetchContext: ...

    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        request: RequestObjectType
    ) -> None:
        """Method generated by attrs for class BaseCursor.
        """
        ...

    toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]]
    _request: typing.Any
    _prev_response: typing.Any
    _seen_ids: typing.Set[str]



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

    @typing.overload
    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        event_type: typing.Any,
        request: toloka.client.search_requests.AssignmentSearchRequest = ...
    ) -> None:
        """Method generated by attrs for class AssignmentCursor.
        """
        ...

    @typing.overload
    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        event_type: typing.Any,
        status: typing.Union[str, toloka.client.assignment.Assignment.Status, typing.List[typing.Union[str, toloka.client.assignment.Assignment.Status]]] = None,
        task_id: typing.Optional[str] = None,
        task_suite_id: typing.Optional[str] = None,
        pool_id: typing.Optional[str] = None,
        user_id: typing.Optional[str] = None,
        id_lt: typing.Optional[str] = None,
        id_lte: typing.Optional[str] = None,
        id_gt: typing.Optional[str] = None,
        id_gte: typing.Optional[str] = None,
        created_lt: typing.Optional[datetime.datetime] = None,
        created_lte: typing.Optional[datetime.datetime] = None,
        created_gt: typing.Optional[datetime.datetime] = None,
        created_gte: typing.Optional[datetime.datetime] = None,
        submitted_lt: typing.Optional[datetime.datetime] = None,
        submitted_lte: typing.Optional[datetime.datetime] = None,
        submitted_gt: typing.Optional[datetime.datetime] = None,
        submitted_gte: typing.Optional[datetime.datetime] = None,
        accepted_lt: typing.Optional[datetime.datetime] = None,
        accepted_lte: typing.Optional[datetime.datetime] = None,
        accepted_gt: typing.Optional[datetime.datetime] = None,
        accepted_gte: typing.Optional[datetime.datetime] = None,
        rejected_lt: typing.Optional[datetime.datetime] = None,
        rejected_lte: typing.Optional[datetime.datetime] = None,
        rejected_gt: typing.Optional[datetime.datetime] = None,
        rejected_gte: typing.Optional[datetime.datetime] = None,
        skipped_lt: typing.Optional[datetime.datetime] = None,
        skipped_lte: typing.Optional[datetime.datetime] = None,
        skipped_gt: typing.Optional[datetime.datetime] = None,
        skipped_gte: typing.Optional[datetime.datetime] = None,
        expired_lt: typing.Optional[datetime.datetime] = None,
        expired_lte: typing.Optional[datetime.datetime] = None,
        expired_gt: typing.Optional[datetime.datetime] = None,
        expired_gte: typing.Optional[datetime.datetime] = None
    ) -> None:
        """Method generated by attrs for class AssignmentCursor.
        """
        ...

    toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]]
    _request: toloka.client.search_requests.AssignmentSearchRequest
    _prev_response: typing.Any
    _seen_ids: typing.Set[str]
    _event_type: toloka.streaming.event.AssignmentEvent.Type


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

    @typing.overload
    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        request: toloka.client.search_requests.TaskSearchRequest = ...
    ) -> None:
        """Method generated by attrs for class TaskCursor.
        """
        ...

    @typing.overload
    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        pool_id: typing.Optional[str] = None,
        overlap: typing.Optional[int] = None,
        id_lt: typing.Optional[str] = None,
        id_lte: typing.Optional[str] = None,
        id_gt: typing.Optional[str] = None,
        id_gte: typing.Optional[str] = None,
        created_lt: typing.Optional[datetime.datetime] = None,
        created_lte: typing.Optional[datetime.datetime] = None,
        created_gt: typing.Optional[datetime.datetime] = None,
        created_gte: typing.Optional[datetime.datetime] = None,
        overlap_lt: typing.Optional[int] = None,
        overlap_lte: typing.Optional[int] = None,
        overlap_gt: typing.Optional[int] = None,
        overlap_gte: typing.Optional[int] = None
    ) -> None:
        """Method generated by attrs for class TaskCursor.
        """
        ...

    toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]]
    _request: toloka.client.search_requests.TaskSearchRequest
    _prev_response: typing.Any
    _seen_ids: typing.Set[str]


class UserBonusCursor(BaseCursor):
    """Iterator over user bonuses by create time.

    Args:
        toloka_client: TolokaClient object that is being used to search user bonuses.
        request: Base request to search user bonuses by.

    Examples:
        Iterate over user bonuses.

        >>> it = UserBonusCursor(toloka_client=toloka_client)
        >>> current_bonuses = list(it)
        >>> # ... new user bonuses could appear ...
        >>> new_bonuses = list(it)  # Contains only new user bonuses, appeared since the previous call.
        ...
    """

    @typing.overload
    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        request: toloka.client.search_requests.UserBonusSearchRequest = ...
    ) -> None:
        """Method generated by attrs for class UserBonusCursor.
        """
        ...

    @typing.overload
    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        user_id: typing.Optional[str] = None,
        private_comment: typing.Optional[str] = None,
        id_lt: typing.Optional[str] = None,
        id_lte: typing.Optional[str] = None,
        id_gt: typing.Optional[str] = None,
        id_gte: typing.Optional[str] = None,
        created_lt: typing.Optional[datetime.datetime] = None,
        created_lte: typing.Optional[datetime.datetime] = None,
        created_gt: typing.Optional[datetime.datetime] = None,
        created_gte: typing.Optional[datetime.datetime] = None
    ) -> None:
        """Method generated by attrs for class UserBonusCursor.
        """
        ...

    toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]]
    _request: toloka.client.search_requests.UserBonusSearchRequest
    _prev_response: typing.Any
    _seen_ids: typing.Set[str]


class UserSkillCursor(BaseCursor):
    """Iterator over UserSkillEvent objects of seleted event_type.

    Args:
        toloka_client: TolokaClient object that is being used to search user skills.
        request: Base request to search user skills by.
        event_type: User skill event's type to search.

    Examples:
        Iterate over user skills acceptances events.

        >>> it = UserSkillCursor(event_type='MODIFIED', toloka_client=toloka_client)
        >>> current_events = list(it)
        >>> # ... new user skills could be set ...
        >>> new_events = list(it)  # Contains only new events, occured since the previous call.
        ...
    """

    @typing.overload
    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        event_type: typing.Any,
        request: toloka.client.search_requests.UserSkillSearchRequest = ...
    ) -> None:
        """Method generated by attrs for class UserSkillCursor.
        """
        ...

    @typing.overload
    def __init__(
        self,
        toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]],
        event_type: typing.Any,
        user_id: typing.Optional[str] = None,
        skill_id: typing.Optional[str] = None,
        id_lt: typing.Optional[str] = None,
        id_lte: typing.Optional[str] = None,
        id_gt: typing.Optional[str] = None,
        id_gte: typing.Optional[str] = None,
        created_lt: typing.Optional[datetime.datetime] = None,
        created_lte: typing.Optional[datetime.datetime] = None,
        created_gt: typing.Optional[datetime.datetime] = None,
        created_gte: typing.Optional[datetime.datetime] = None,
        modified_lt: typing.Optional[datetime.datetime] = None,
        modified_lte: typing.Optional[datetime.datetime] = None,
        modified_gt: typing.Optional[datetime.datetime] = None,
        modified_gte: typing.Optional[datetime.datetime] = None
    ) -> None:
        """Method generated by attrs for class UserSkillCursor.
        """
        ...

    toloka_client: typing.Union[toloka.client.TolokaClient, toloka.util.async_utils.AsyncMultithreadWrapper[toloka.client.TolokaClient]]
    _request: toloka.client.search_requests.UserSkillSearchRequest
    _prev_response: typing.Any
    _seen_ids: typing.Set[str]
    _event_type: toloka.streaming.event.UserSkillEvent.Type


class UserRestrictionCursor(BaseCursor):
    """Iterator over user restrictions by create time.

    Args:
        toloka_client: TolokaClient object that is being used to search user restrictions.
        request: Base request to search user restrictions.

    Examples:
        Iterate over user restrictions in project.

        >>> it = UserRestrictionCursor(toloka_client=toloka_client, project_id=my_proj_id)
        >>> current_restrictions = list(it)
        >>> # ... new restrictions could appear ...
        >>> new_restrictions = list(it)  # Contains only new user restrictions, appeared since the previous call.
        ...
    """

    @typing.overload
    def __init__(
        self,
        toloka_client: TolokaClientSyncOrAsyncType,
        request: toloka.client.search_requests.UserRestrictionSearchRequest = ...
    ) -> None:
        """Method generated by attrs for class UserRestrictionCursor.
        """
        ...

    @typing.overload
    def __init__(
        self,
        toloka_client: TolokaClientSyncOrAsyncType,
        scope: typing.Optional[toloka.client.user_restriction.UserRestriction.Scope] = None,
        user_id: typing.Optional[str] = None,
        project_id: typing.Optional[str] = None,
        pool_id: typing.Optional[str] = None,
        id_lt: typing.Optional[str] = None,
        id_lte: typing.Optional[str] = None,
        id_gt: typing.Optional[str] = None,
        id_gte: typing.Optional[str] = None,
        created_lt: typing.Optional[datetime.datetime] = None,
        created_lte: typing.Optional[datetime.datetime] = None,
        created_gt: typing.Optional[datetime.datetime] = None,
        created_gte: typing.Optional[datetime.datetime] = None
    ) -> None:
        """Method generated by attrs for class UserRestrictionCursor.
        """
        ...

    toloka_client: TolokaClientSyncOrAsyncType
    _request: toloka.client.search_requests.UserRestrictionSearchRequest
    _prev_response: typing.Any
    _seen_ids: typing.Any


class MessageThreadCursor(BaseCursor):
    """Iterator over messages by create time.

    Args:
        toloka_client: TolokaClient object that is being used to search messages.
        request: Base request to search messages.

    Examples:
        Iterate over all messages.

        >>> it = MessageThreadCursor(toloka_client=toloka_client)
        >>> all_messages = list(it)
        >>> # ... new messages could appear ...
        >>> new_messages = list(it)  # Contains only new messages, appeared since the previous call.
        ...
    """

    @typing.overload
    def __init__(
        self,
        toloka_client: TolokaClientSyncOrAsyncType,
        request: toloka.client.search_requests.MessageThreadSearchRequest = ...
    ) -> None:
        """Method generated by attrs for class MessageThreadCursor.
        """
        ...

    @typing.overload
    def __init__(
        self,
        toloka_client: TolokaClientSyncOrAsyncType,
        folder: typing.Union[str, toloka.client.message_thread.Folder, typing.List[typing.Union[str, toloka.client.message_thread.Folder]]] = None,
        folder_ne: typing.Union[str, toloka.client.message_thread.Folder, typing.List[typing.Union[str, toloka.client.message_thread.Folder]]] = None,
        id_lt: typing.Optional[str] = None,
        id_lte: typing.Optional[str] = None,
        id_gt: typing.Optional[str] = None,
        id_gte: typing.Optional[str] = None,
        created_lt: typing.Optional[datetime.datetime] = None,
        created_lte: typing.Optional[datetime.datetime] = None,
        created_gt: typing.Optional[datetime.datetime] = None,
        created_gte: typing.Optional[datetime.datetime] = None
    ) -> None:
        """Method generated by attrs for class MessageThreadCursor.
        """
        ...

    toloka_client: TolokaClientSyncOrAsyncType
    _request: toloka.client.search_requests.MessageThreadSearchRequest
    _prev_response: typing.Any
    _seen_ids: typing.Any
