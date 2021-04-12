__all__ = [
    'SortItemSelf',
    'SortItemsSelf',
    'SortOrder',
    'BaseSortItem',
    'BaseSortItems',
    'SearchRequestMetaclass',
    'BaseSearchRequest',
    'ProjectSearchRequest',
    'ProjectSortItems',
    'PoolSearchRequest',
    'PoolSortItems',
    'TrainingSearchRequest',
    'TrainingSortItems',
    'SkillSearchRequest',
    'SkillSortItems',
    'AssignmentSearchRequest',
    'AssignmentSortItems',
    'AggregatedSolutionSearchRequest',
    'AggregatedSolutionSortItems',
    'TaskSearchRequest',
    'TaskSortItems',
    'TaskSuiteSearchRequest',
    'TaskSuiteSortItems',
    'AttachmentSearchRequest',
    'AttachmentSortItems',
    'UserSkillSearchRequest',
    'UserSkillSortItems',
    'UserRestrictionSearchRequest',
    'UserRestrictionSortItems',
    'UserBonusSearchRequest',
    'UserBonusSortItems',
    'MessageThreadSearchRequest',
    'MessageThreadSortItems'
]
import datetime
from enum import Enum, unique, auto
from typing import Optional, TypeVar, Type, Union, List, get_type_hints, cast

import attr

from ._converter import converter, structure, unstructure
from .assignment import Assignment
from .attachment import Attachment
from .message_thread import Folder
from .pool import Pool
from .project import Project
from .training import Training
from .user_restriction import UserRestriction
from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass

SortItemSelf = TypeVar('SortItemSelf', bound='BaseSortItem')
SortItemsSelf = TypeVar('SortItemsSelf', bound='BaseSortItems')


@unique
class SortOrder(Enum):
    ASCENDING = auto()
    DESCENDING = auto()


class BaseSortItem(BaseTolokaObject):

    def unstructure(self):
        if self.order == SortOrder.DESCENDING:
            return f'-{self.field.value}'
        return f'{self.field.value}'

    @classmethod
    def structure(cls: Type[SortItemSelf], value: Union[SortItemSelf, str]) -> SortItemSelf:
        if isinstance(value, cls):
            return value

        value = cast(str, value)
        if value.startswith('-'):
            return cls(structure(value[1:], cls.SortField), SortOrder.DESCENDING)  # type: ignore
        return cls(structure(value, cls.SortField), SortOrder.ASCENDING)  # type: ignore

    @staticmethod
    def _create_sort_field_enum(sort_fields: List[str]):
        namespace = {field.upper(): field for field in sort_fields}
        return unique(Enum('SortField', namespace))  # type: ignore

    @classmethod
    def for_fields(cls, sort_fields: List[str]):
        sort_field_enum = cls._create_sort_field_enum(sort_fields)
        namespace = {
            'SortField': sort_field_enum,
            'order': SortOrder.ASCENDING,
            '__annotations__': {
                'field': sort_field_enum,
                'order': SortOrder,
            },
        }

        subclass = BaseTolokaObjectMetaclass('SortItem', (cls,), namespace, kw_only=False)
        subclass.__module__ = __name__
        return subclass


class BaseSortItems(BaseTolokaObject):

    def unstructure(self):
        return ','.join(unstructure(item) for item in self.items)

    @classmethod
    def structure(cls, items):
        if isinstance(items, cls):
            return items
        return cls(items=items)

    @classmethod
    def for_fields(cls, name: str, sort_fields: List[str], docstring: Optional[str] = None):
        sort_item_class: Type = BaseSortItem.for_fields(sort_fields)

        def items_converter(items):
            if isinstance(items, sort_items_class):
                return items
            if isinstance(items, str):
                items = items.split(',')
            return [sort_item_class.structure(item) for item in items]

        namespace = {
            'SortItem': sort_item_class,
            '__annotations__': {'items': List[sort_item_class]},  # type: ignore
            'items': attr.attrib(converter=items_converter),
        }
        sort_items_class = BaseTolokaObjectMetaclass(name, (BaseSortItems,), namespace, kw_only=False)
        sort_items_class.__module__ = __name__
        sort_items_class.__doc__ = docstring
        return sort_items_class


class SearchRequestMetaclass(BaseTolokaObjectMetaclass):

    def __new__(mcs, name, bases, namespace, kw_only=False, **kwargs):
        compare_fields_class = namespace['CompareFields']
        annotations = namespace.setdefault('__annotations__', {})

        # For every comparable field creating a corresponding attribute
        for field_name, field_type in get_type_hints(compare_fields_class).items():
            for suffix in 'lt', 'lte', 'gt', 'gte':
                condition_field = f'{field_name}_{suffix}'
                namespace[condition_field] = None
                annotations[condition_field] = Optional[field_type]

        # Building class
        subclass = super().__new__(mcs, name, bases, namespace, kw_only=kw_only, **kwargs)
        subclass.__module__ = __name__
        return subclass


class BaseSearchRequest(BaseTolokaObject, metaclass=SearchRequestMetaclass):
    """Base class for all search request classes
    """

    class CompareFields:
        pass


class ProjectSearchRequest(BaseSearchRequest):
    """Parameters for searching projects

    Attributes:
        status: Status of the project, from Project.ProjectStatus:
            * ACTIVE
            * ARCHIVED
        id_lt: Projects with an ID less than the specified value.
        id_lte: Projects with an ID less than or equal to the specified value.
        id_gt: Projects with an ID greater than the specified value.
        id_gte: Projects with an ID greater than or equal to the specified value.
        created_lt: Projects created before the specified date.
        created_lte: Projects created before or on the specified date.
        created_gt: Projects created after the specified date.
        created_gte: Projects created after or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime

    status: Project.ProjectStatus


ProjectSortItems = BaseSortItems.for_fields(
    'ProjectSortItems', ['id', 'created', 'public_name', 'private_comment'],
    # docstring
    """Parameters for sorting project search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Project ID in ascending order.
            * created - Project creation date in UTC in yyyy-MM-DD format (ascending).
            * public_name - Project name (in alphabetical order).
            * private_comment - Comment on the project (in alphabetical order).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.ProjectSortItems(['-public_name', 'id'])
        >>> result = toloka_client.find_projects(status='ACTIVE', sort=sort, limit=50)
        ...
    """
)


class PoolSearchRequest(BaseSearchRequest):
    """Parameters for searching pools

    Attributes:
        status: Pool status
            * OPEN
            * CLOSED
            * ARCHIVED
            * LOCKED
        project_id: ID of the project to which the pool is attached.
        id_lt: Pools with an ID less than the specified value.
        id_lte: Pools with an ID less than or equal to the specified value.
        id_gt: Pools with an ID greater than the specified value.
        id_gte: Pools with an ID greater than or equal to the specified value.
        created_lt: Pools created before the specified date.
        created_lte: Pools created before or on the specified date.
        created_gt: Pools created after the specified date.
        created_gte: Pools created after or on the specified date.
        last_started_lt: Pools that were last opened before the specified date.
        last_started_lte: Pools that were last opened on or before the specified date.
        last_started_gt: Pools that were last opened after the specified date.
        last_started_gte: Pools that were last opened on or after the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime
        last_started: datetime.datetime

    status: Pool.Status
    project_id: str


PoolSortItems = BaseSortItems.for_fields(
    'PoolSortItems', ['id', 'created', 'last_started'],
    # docstring
    """Parameters for sorting pool search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Pool ID in ascending order.
            * created - Pool creation date in UTC in yyyy-MM-DD format (ascending).
            * last_started - The date the pool was last started (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.PoolSortItems(['-last_started', 'id'])
        >>> result = toloka_client.find_pools(status='OPEN', sort=sort, limit=50)
        ...
    """

)


class TrainingSearchRequest(BaseSearchRequest):
    """Parameters for searching training pools

    Attributes:
        status: Training pool status:
            * OPEN
            * CLOSED
            * ARCHIVED
            * LOCKED
        project_id: ID of the project to which the training pool is attached.
        id_lt: Training pools with an ID less than the specified value.
        id_lte: Training pools with an ID less than or equal to the specified value.
        id_gt: Training pools with an ID greater than the specified value.
        id_gte: Training pools with an ID greater than or equal to the specified value.
        created_lt: Training pools created before the specified date.
        created_lte: Training pools created before or on the specified date.
        created_gt: Training pools created after the specified date.
        created_gte: Training pools created after or on the specified date.
        last_started_lt: Training pools that were last opened before the specified date.
        last_started_lte: Training pools that were last opened on or before the specified date.
        last_started_gt: Training pools that were last opened after the specified date.
        last_started_gte: Training pools that were last opened on or after the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime
        last_started: datetime.datetime

    status: Training.Status
    project_id: str


TrainingSortItems = BaseSortItems.for_fields(
    'TrainingSortItems', ['id', 'created', 'last_started'],
    # docstring
    """Parameters for sorting training pool search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Training pool ID in ascending order.
            * created - Training pool creation date in UTC in yyyy-MM-DD format (ascending).
            * last_started - The date the pool was last started (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.TrainingSortItems(['-last_started', 'id'])
        >>> result = toloka_client.find_trainings(status='OPEN', sort=sort, limit=50)
        ...
    """
)


class SkillSearchRequest(BaseSearchRequest):
    """Parameters for searching skill

    Attributes:
        name: Skill name.
        id_lt: Skills with an ID less than the specified value.
        id_lte: Skills with an ID less than or equal to the specified value.
        id_gt: Skills with an ID greater than the specified value.
        id_gte: Skills with an ID greater than or equal to the specified value.
        created_lt: Skills created before the specified date.
        created_lte: Skills created before or on the specified date.
        created_gt: Skills created after the specified date.
        created_gte: Skills created on or after the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime

    name: str


SkillSortItems = BaseSortItems.for_fields(
    'SkillSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting skill search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Skill ID in ascending order.
            * created - Skill creation date in UTC in yyyy-MM-DD format (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.SkillSortItems(['-created', 'id'])
        >>> result = toloka_client.find_skills(name='Image annotation', sort=sort, limit=10)
        ...
    """
)


class AssignmentSearchRequest(BaseSearchRequest):
    """Parameters for searching assignment

    Attributes:
        status: Status of an assigned task suite (Detailed status description in Assignment.Status):
            * ACTIVE
            * SUBMITTED
            * ACCEPTED
            * REJECTED
            * SKIPPED
            * EXPIRED
        task_id: The task ID in suites generated automatically using "smart mixing".
            You will get responses for task suites that contain the specified task.
        task_suite_id: ID of a task suite.
        pool_id: Pool ID.
        user_id: Performer ID.
        id_lt: Task suites with an assignment ID less than the specified value.
        id_lte: Task suites with an assignment ID less than or equal to the specified value.
        id_gt: Task suites with an assignment ID greater than the specified value.
        id_gte: Task suites with an assignment ID greater than or equal to the specified value.
        created_lt: Task suites assigned before the specified date.
        created_lte: Task suites assigned before or on the specified date.
        created_gt: Task suites assigned after the specified date.
        created_gte: Task suites assigned after or on the specified date.
        submitted_lt: Task suites completed before the specified date.
        submitted_lte: Task suites completed before or on the specified date.
        submitted_gt: Task suites completed after the specified date.
        submitted_gte: Task suites completed after or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime
        submitted: datetime.datetime

    def _list_converter(value):
        if value is None:
            return value
        if isinstance(value, str):
            value = value.split(',')
            value = [item.strip() for item in value]
        if not isinstance(value, list):
            value = [value]
        return [Assignment.Status(item) for item in value]

    def _list_setter(self, attribute, value):
        return AssignmentSearchRequest._list_converter(value)

    def unstructure(self) -> Optional[dict]:
        data = super().unstructure()

        if self.status is not None:
            data['status'] = ','.join(converter.unstructure(item) for item in self.status)

        return data

    status: List[Assignment.Status] = attr.attrib(converter=_list_converter, on_setattr=_list_setter)
    task_id: str
    task_suite_id: str
    pool_id: str
    user_id: str


AssignmentSortItems = BaseSortItems.for_fields(
    'AssignmentSortItems', ['id', 'created', 'submitted'],
    # docstring
    """Parameters for sorting assignment search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - ID for issuing a set of tasks (in ascending order).
            * created - Date of issue of the set of tasks in UTC in ISO 8601 format YYYY-MM-DDThh:mm:ss[.sss] (ascending).
            * submitted - Date of completion of the set of tasks in UTC in ISO 8601 format YYYY-MM-DDThh:mm:ss[.sss] (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.AssignmentSortItems(['-submitted', 'id'])
        >>> result = toloka_client.find_assignments(status='SUBMITTED', sort=sort, limit=10)
        ...
    """
)


class AggregatedSolutionSearchRequest(BaseSearchRequest):
    """Parameters for searching aggregated solution

    Attributes:
        task_id_lt: Jobs with an ID greater than the specified value.
        task_id_lte: Jobs with an ID greater than or equal to the specified value.
        task_id_gt: Jobs with an ID less than the specified value.
        task_id_gte: Jobs with an ID less than or equal to the specified value.
    """

    class CompareFields:
        task_id: str


AggregatedSolutionSortItems = BaseSortItems.for_fields(
    'AggregatedSolutionSortItems', ['task_id'],
    # docstring
    """Parameters for sorting aggregated solution search results

    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * task_id - In ascending order.
    """
)


class TaskSearchRequest(BaseSearchRequest):
    """Parameters for searching tasks

    Attributes:
        pool_id: ID of the pool to get tasks from.
        overlap: Tasks with an overlap equal to the specified value.
        id_lt: Tasks with an ID less than the specified value.
        id_lte: Tasks with an ID less than or equal to the specified value.
        id_gt: Tasks with an ID greater than the specified value.
        id_gte: Tasks with an ID greater than or equal to the specified value.
        created_lt: Tasks created before the specified date.
        created_lte: Tasks created before or on the specified date.
        created_gt: Tasks created after the specified date.
        created_gte: Tasks created after or on the specified date.
        overlap_lt: Tasks with an overlap less than the specified value.
        overlap_lte: Tasks with an overlap equal to the specified value.
        overlap_gt: Tasks with an overlap greater than the specified value.
        overlap_gte: Tasks with an overlap equal to the specified value.
    """

    class CompareFields:
        id: str
        created: datetime.datetime
        overlap: int

    pool_id: str
    overlap: int


TaskSortItems = BaseSortItems.for_fields(
    'TaskSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting task search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Job ID (in ascending order).
            * created - Date of creation of the task in UTC in the format YYYY-MM-DD (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.TaskSortItems(['-created', 'id'])
        >>> result = toloka_client.find_tasks(pool_id=my_pretty_pool_id, sort=sort, limit=10)
        ...
    """
)


class TaskSuiteSearchRequest(BaseSearchRequest):
    """Parameters for searching task suites

    Attributes:
        task_id: The task ID in suites generated automatically using "smart mixing".
            You will get task suites that contain the specified task.
        pool_id: ID of the pool to get task suites from.
        overlap: Suites with an overlap equal to the specified value.
        id_lt: Task suites with an ID less than the specified value.
        id_lte: Task suites with an ID less than or equal to the specified value.
        id_gt: Task suites with an ID greater than the specified value.
        id_gte: Task suites with an ID greater than or equal to the specified value.
        created_lt: Task suites created before the specified date.
        created_lte: Task suites created before or on the specified date.
        created_gt: Task suites created after the specified date.
        created_gte: Task suites created after or on the specified date.
        overlap_lt: Suites with an overlap less than the specified value.
        overlap_lte: Suites with an overlap less than or equal to the specified value.
        overlap_gt: Suites with an overlap greater than the specified value.
        overlap_gte: Suites with an overlap greater than or equal to the specified value.
    """

    class CompareFields:
        id: str
        created: datetime.datetime
        overlap: int

    task_id: str
    pool_id: str
    overlap: int


TaskSuiteSortItems = BaseSortItems.for_fields(
    'TaskSuiteSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting task suite search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Task set ID (in ascending order).
            * created - Date of creation of the set of tasks in UTC in the format YYYY-MM-DD (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.TaskSuiteSortItems(['-created', 'id'])
        >>> result = toloka_client.find_task_suites(pool_id=my_pretty_pool_id, sort=sort, limit=10)
        ...
    """
)


class AttachmentSearchRequest(BaseSearchRequest):
    """Parameters for searching attachment

    Attributes:
        name: File name.
        type: Attachment type. Currently the key can have only one value - ASSIGNMENT_ATTACHMENT.
        user_id: ID of the user who uploaded the file(s).
        assignment_id: Assignment ID.
        pool_id: Pool ID.
        owner_id: Optional[str]
        owner_company_id: Optional[str]
        id_lt: Files with an ID less than the specified value.
        id_lte: Files with an ID less than or equal to the specified value.
        id_gt: Files with an ID greater than the specified value.
        id_gte: Files with an ID greater than or equal to the specified value.
        created_lt: Files uploaded by users before the specified date.
        created_lte: Files uploaded by users before or on the specified date.
        created_gt: Files uploaded by users after the specified date.
        created_gte: Files uploaded by users after or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime

    name: str
    type: Attachment.Type
    user_id: str
    assignment_id: str
    pool_id: str

    owner_id: str
    owner_company_id: str


AttachmentSortItems = BaseSortItems.for_fields(
    'AttachmentSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting attachment search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - File ID in ascending order.
            * created - Date of sending the file in UTC in the yyyy-MM-DD format (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.AttachmentSortItems(['-created', 'id'])
        >>> result = toloka_client.find_attachments(pool_id=my_pretty_pool_id, sort=sort, limit=10)
        ...
    """
)


class UserSkillSearchRequest(BaseSearchRequest):
    """Parameters for searching user skill

    Attributes:
        name: Skill name.
        user_id: Performer ID.
        skill_id: Skill ID.
        id_lt: Skills with an ID less than the specified value.
        id_lte: Skills with an ID less than or equal to the specified value.
        id_gt: Skills with an ID greater than the specified value.
        id_gte: Skills with an ID greater than or equal to the specified value.
        created_lt: Skills created before the specified date.
        created_lte: Skills created before or on the specified date.
        created_gt: Skills created after the specified date.
        created_gte: Skills created on or after the specified date.
        modified_lt: Skills that changed before the specified date.
        modified_lte: Skills that changed before the specified date.
        modified_gt: Skills changed after the specified date.
        modified_gte: Skills created on or after the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime
        modified: datetime.datetime

    name: str

    user_id: str
    skill_id: str


UserSkillSortItems = BaseSortItems.for_fields(
    'UserSkillSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting user skill search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Skill ID in ascending order.
            * created - Date the skill was created in UTC in the yyyy-MM-DD format (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.UserSkillSortItems(['-created', 'id'])
        >>> result = toloka_client.find_user_skills(skill_id=my_useful_skill_id, sort=sort, limit=10)
        ...
    """
)


class UserRestrictionSearchRequest(BaseSearchRequest):
    """Parameters for searching user restriction

    Attributes:
        scope: The scope of the ban
            * ALL_PROJECTS
            * PROJECT
            * POOL
        user_id: Performer ID.
        project_id: The ID of the project that is blocked.
        pool_id: The ID of the pool that is blocked.
        id_lt: Bans with an ID less than the specified value.
        id_lte: Bans with an ID less than or equal to the specified value.
        id_gt: Bans with an ID greater than the specified value.
        id_gte: Bans with an ID greater than or equal to the specified value.
        created_lt: Bans created before the specified date.
        created_lte: Bans created before or on the specified date.
        created_gt: Bans created after the specified date.
        created_gte: Bans created after or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime

    scope: UserRestriction.Scope
    user_id: str
    project_id: str
    pool_id: str


UserRestrictionSortItems = BaseSortItems.for_fields(
    'UserRestrictionSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting user restriction search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - User restriction ID in ascending order.
            * created - Creation date in UTC format yyyy-MM-DD (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.UserRestrictionSortItems(['-created', 'id'])
        >>> result = toloka_client.find_user_restrictions(pool_id=my_pretty_pool_id, sort=sort, limit=10)
        ...
    """
)


class UserBonusSearchRequest(BaseSearchRequest):
    """Parameters for searching user bonus

    Attributes:
        user_id: Performer ID.
        private_comment: Comments for the requester.
        id_lt: Bonuses with an ID less than the specified value.
        id_lte: Bonuses with an ID less than or equal to the specified value.
        id_gt: Bonuses with an ID greater than the specified value.
        id_gte: Bonuses with an ID greater than or equal to the specified value.
        created_lt: Bonuses awarded before the specified date.
        created_lte: Bonuses awarded before or on the specified date.
        created_gt: Bonuses awarded after the specified date.
        created_gte: Bonuses awarded after or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime

    user_id: str
    private_comment: str


UserBonusSortItems = BaseSortItems.for_fields(
    'UserBonusSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting user bonus search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Bonus ID in ascending order.
            * created - Creation date in UTC format yyyy-MM-DD (ascending).

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.UserBonusSortItems(['-created', 'id'])
        >>> result = toloka_client.find_user_bonuses(user_id=best_performer_id, sort=sort, limit=10)
        ...
    """
)


class MessageThreadSearchRequest(BaseSearchRequest):
    """Parameters for searching message threads

    Attributes:
        folder: Folders to search for the thread
        folder_ne: Folders to not search for the thread
        id_lt: Threads with an ID less than the specified value.
        id_lte: Threads with an ID less than or equal to the specified value.
        id_gt: Threads with an ID greater than the specified value.
        id_gte: Threads with an ID greater than or equal to the specified value.
        created_lt: Threads created before the specified date.
        created_lte: Threads created before or on the specified date.
        created_gt: Threads created after the specified date.
        created_gte: Threads created after or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime

    def _list_converter(value):
        if value is None:
            return value
        if isinstance(value, str):
            value = value.split(',')
            value = [item.strip() for item in value]
        if not isinstance(value, list):
            value = [value]
        return [Folder(item) for item in value]

    def _list_setter(self, attribute, value):
        return MessageThreadSearchRequest._list_converter(value)

    def unstructure(self) -> Optional[dict]:
        data = super().unstructure()
        if self.folder is not None:
            data['folder'] = ','.join(converter.unstructure(item) for item in self.folder)
        if self.folder_ne is not None:
            data['folder_ne'] = ','.join(converter.unstructure(item) for item in self.folder_ne)
        return data

    folder: List[Folder] = attr.attrib(converter=_list_converter, on_setattr=_list_setter)
    folder_ne: List[Folder] = attr.attrib(converter=_list_converter, on_setattr=_list_setter)


MessageThreadSortItems = BaseSortItems.for_fields(
    'MessageThreadSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting message thread search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Thread ID in ascending order.
            * created - Creation date in UTC format yyyy-MM-DD (ascending).
    """
)
