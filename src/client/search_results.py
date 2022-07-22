__all__ = [
    'AggregatedSolutionSearchResult',
    'AssignmentSearchResult',
    'AttachmentSearchResult',
    'MessageThreadSearchResult',
    'ProjectSearchResult',
    'PoolSearchResult',
    'SkillSearchResult',
    'TaskSearchResult',
    'TaskSuiteSearchResult',
    'TrainingSearchResult',
    'UserBonusSearchResult',
    'UserRestrictionSearchResult',
    'UserSkillSearchResult',
    'WebhookSubscriptionSearchResult',
    'OperationSearchResult',
    'AppProjectSearchResult',
    'AppSearchResult',
    'AppItemSearchResult',
    'AppBatchSearchResult'
]
from typing import Type, List, Optional
from .aggregation import AggregatedSolution
from .app import App, AppItem, AppProject, AppBatch
from .assignment import Assignment
from .attachment import Attachment
from .message_thread import MessageThread
from .operations import Operation
from .pool import Pool
from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass
from .project import Project
from .skill import Skill
from .task import Task
from .task_suite import TaskSuite
from .training import Training
from .user_bonus import UserBonus
from .user_restriction import UserRestriction
from .user_skill import UserSkill
from .webhook_subscription import WebhookSubscription


def _create_search_result_class_for(type_: Type, docstring: Optional[str] = None, items_field: str = 'items'):
    cls = BaseTolokaObjectMetaclass(
        f'{type_.__name__}SearchResult',
        (BaseTolokaObject,),
        {'__annotations__': {items_field: List[type_], 'has_more': bool}},
    )
    cls.__module__ = __name__
    cls.__doc__ = docstring
    return cls


AggregatedSolutionSearchResult = _create_search_result_class_for(
    AggregatedSolution,
    """The list of found AggregatedSolutions and whether there is something else on the original request

    Attributes:
        items: List of found AggregatedSolution
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
AssignmentSearchResult = _create_search_result_class_for(
    Assignment,
    """The list of found assignments.

    The number of assignments in the list is limited by the [find_assignments](toloka.client.TolokaClient.find_assignments.md) method.

    Attributes:
        items: The list of found assignments.
        has_more: More items flag:
            * `True` — Not all assignments matching search criteria are returned in the `items` due to the limit.
            * `False` — All matching assignments are in the `items`.
    """
)
AttachmentSearchResult = _create_search_result_class_for(
    Attachment,
    """The list of found attachments and whether there is something else on the original request

    It's better to use TolokaClient.get_attachments(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found Attachment
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
MessageThreadSearchResult = _create_search_result_class_for(
    MessageThread,
    """The list of found message chains and whether there is something else on the original request

    It's better to use TolokaClient.get_message_threads(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found MessageThread
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
ProjectSearchResult = _create_search_result_class_for(
    Project,
    """The list of found projects and whether there is something else on the original request

    It's better to use TolokaClient.get_projects(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found projects
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
PoolSearchResult = _create_search_result_class_for(
    Pool,
    """The list of found pools and whether there is something else on the original request

    It's better to use TolokaClient.get_pools(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found pools
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
SkillSearchResult = _create_search_result_class_for(
    Skill,
    """The list of found skills and whether there is something else on the original request

    It's better to use TolokaClient.get_skill(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found skills
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
TaskSearchResult = _create_search_result_class_for(
    Task,
    """The list of found tasks and whether there is something else on the original request

    It's better to use TolokaClient.get_tasks(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found tasks
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
TaskSuiteSearchResult = _create_search_result_class_for(
    TaskSuite,
    """The list of found sets of tasks and whether there is something else on the original request

    It's better to use TolokaClient.get_task_suites(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found sets of tasks
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
TrainingSearchResult = _create_search_result_class_for(
    Training,
    """The list of found training pools and whether there is something else on the original request

    It's better to use TolokaClient.get_trainings(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found training pools
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
UserBonusSearchResult = _create_search_result_class_for(
    UserBonus,
    """The list of found `UserBonus` instances and whether there is something else on the original request

    It's better to use TolokaClient.get_user_bonuses(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found `UserBonus` instances
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
UserRestrictionSearchResult = _create_search_result_class_for(
    UserRestriction,
    """The list of found Toloker restrictions and whether there is something else on the original request

    It's better to use TolokaClient.get_user_restrictions(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found Toloker restrictions
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
UserSkillSearchResult = _create_search_result_class_for(
    UserSkill,
    """The list of found Toloker skills and whether there is something else on the original request

    It's better to use TolokaClient.get_user_skills(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found Toloker skills
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
WebhookSubscriptionSearchResult = _create_search_result_class_for(
    WebhookSubscription,
    """The list of found subscriptions and whether there is something else on the original request

    It's better to use TolokaClient.get_webhook_subscriptions(),
    which already implements the correct handling of the search result.

    Attributes:
        items: List of found subscriptions
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
OperationSearchResult = _create_search_result_class_for(
    Operation,
    """The list of found operations and whether there is something else on the original request

    It's better to use TolokaClient.get_operations(),
    which already implements the correct handling of the search result.

    Attributes:
        items: List of found operations
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
AppProjectSearchResult = _create_search_result_class_for(
    AppProject,
    items_field='content',
    docstring="""The result of searching App projects.

    Attributes:
        content: A list with found App projects.
        has_more: A flag showing whether there are more matching projects.
            * True — There are more matching projects, not included in `content` due to the limit set in the search request.
            * False — `content` contains all matching projects.
    """
)
AppSearchResult = _create_search_result_class_for(
    App,
    items_field='content',
    docstring="""The result of searching App projects.

    Attributes:
        content: A list with found App solutions.
        has_more: A flag showing whether there are more matching solutions.
            * True — There are more matching solutions, not included in `content` due to the limit set in the search request.
            * False — `content` contains all matching solutions.
    """
)
AppItemSearchResult = _create_search_result_class_for(
    AppItem,
    items_field='content',
    docstring="""The result of searching App task items.

    Attributes:
        content: A list with found App task items.
        has_more: A flag showing whether there are more matching task items.
            * True — There are more matching task items, not included in `content` due to the limit set in the search request.
            * False — `content` contains all matching task items.
    """
)
AppBatchSearchResult = _create_search_result_class_for(
    AppBatch,
    items_field='content',
    docstring="""The result of searching batches in an App project.

    Attributes:
        content: A list with found App batches.
        has_more: A flag showing whether there are more matching batches.
            * True — There are more matching batches, not included in `content` due to the limit set in the search request.
            * False — `content` contains all matching batches.
    """
)
