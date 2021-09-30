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
from .pool import Pool
from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass
from .project import Project
from .training import Training
from .skill import Skill
from .task import Task
from .task_suite import TaskSuite
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
    """The list of found assignments and whether there is something else on the original request

    It's better to use TolokaClient.get_assignments(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found assignments
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
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
    """The list of found user bonuses and whether there is something else on the original request

    It's better to use TolokaClient.get_user_bonuses(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found user bonuses
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
UserRestrictionSearchResult = _create_search_result_class_for(
    UserRestriction,
    """The list of found user restrictions and whether there is something else on the original request

    It's better to use TolokaClient.get_user_restrictions(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found user restrictions
        has_more: Whether the list is complete:
            * True - Not all elements are included in the output due to restrictions in the limit parameter.
            * False - The output lists all the items.
    """
)
UserSkillSearchResult = _create_search_result_class_for(
    UserSkill,
    """The list of found user skills and whether there is something else on the original request

    It's better to use TolokaClient.get_user_skills(), which already implements the correct handling of the search result.

    Attributes:
        items: List of found user skills
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
AppProjectSearchResult = _create_search_result_class_for(
    AppProject,
    items_field='content'
)
AppSearchResult = _create_search_result_class_for(
    App,
    items_field='content'
)
AppItemSearchResult = _create_search_result_class_for(
    AppItem,
    items_field='content'
)
AppBatchSearchResult = _create_search_result_class_for(
    AppBatch,
    items_field='content'
)
