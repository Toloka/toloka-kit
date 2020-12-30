from typing import Any, Dict, List, Optional

from .aggregation import AggregatedSolution
from .assignment import Assignment
from .attachment import Attachment
from .message_thread import MessageThread
from .pool import Pool
from .primitives.base import BaseTolokaObject
from .project import Project
from .skill import Skill
from .task import Task
from .task_suite import TaskSuite
from .user_bonus import UserBonus
from .user_restriction import UserRestriction
from .user_skill import UserSkill


class AggregatedSolutionSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[AggregatedSolution]]
    has_more: Optional[bool]

class AssignmentSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[Assignment]]
    has_more: Optional[bool]

class AttachmentSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[Attachment]]
    has_more: Optional[bool]

class MessageThreadSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[MessageThread]]
    has_more: Optional[bool]

class ProjectSearchResult(BaseTolokaObject):
    """ProjectSearchResult

    Attributes:
        items: List of found projects
        has_more: Whether the list is complete:
            * true — Not all elements are included in the output due to restrictions in the limit parameter.
            * false — The output lists all the items.
    """

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[Project]]
    has_more: Optional[bool]

class PoolSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[Pool]]
    has_more: Optional[bool]

class SkillSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[Skill]]
    has_more: Optional[bool]

class TaskSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[Task]]
    has_more: Optional[bool]

class TaskSuiteSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[TaskSuite]]
    has_more: Optional[bool]

class UserBonusSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[UserBonus]]
    has_more: Optional[bool]

class UserRestrictionSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[UserRestriction]]
    has_more: Optional[bool]

class UserSkillSearchResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[UserSkill]]
    has_more: Optional[bool]
