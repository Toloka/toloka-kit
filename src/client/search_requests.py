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
    'MessageThreadSortItems',
    'WebhookSubscriptionSearchRequest',
    'WebhookSubscriptionSortItems',
    'AppProjectSearchRequest',
    'AppProjectSortItems',
    'AppSearchRequest',
    'AppSortItems',
    'AppItemSearchRequest',
    'AppItemSortItems',
    'AppBatchSearchRequest',
    'AppBatchSortItems',
]
import datetime
from enum import Enum, unique, auto
from typing import Optional, TypeVar, Type, Union, List, get_type_hints, cast

import attr

from ._converter import converter, structure, unstructure
from .app import AppItem, AppProject, AppBatch
from .assignment import Assignment
from .attachment import Attachment
from .message_thread import Folder
from .pool import Pool
from .project import Project
from .training import Training
from .user_restriction import UserRestriction
from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass
from .webhook_subscription import WebhookSubscription

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
    def _create_sort_field_enum(qualname: str, sort_fields: List[str]):
        namespace = {field.upper(): field for field in sort_fields}
        namespace['__qualname__'] = qualname
        return unique(Enum(qualname.split('.')[-1], namespace))  # type: ignore

    @classmethod
    def for_fields(cls, qualname: str, sort_fields: List[str]):
        sort_field_enum = cls._create_sort_field_enum(f'{qualname}.SortField', sort_fields)
        namespace = {
            'SortField': sort_field_enum,
            'order': SortOrder.ASCENDING,
            '__qualname__': qualname,
            '__annotations__': {
                'field': sort_field_enum,
                'order': SortOrder,
            },
        }

        subclass = BaseTolokaObjectMetaclass(qualname.split('.')[-1], (cls,), namespace, kw_only=False)
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
    def for_fields(cls, qualname: str, sort_fields: List[str], docstring: Optional[str] = None):
        sort_item_class: Type = BaseSortItem.for_fields(f'{qualname}.SortItem', sort_fields)

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
            '__qualname__': qualname,
        }
        sort_items_class = BaseTolokaObjectMetaclass(qualname.split('.')[-1], (BaseSortItems,), namespace, kw_only=False)
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

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Project ID in ascending order.
            * created — Project creation date.
            * public_name — Project name (in alphabetical order).
            * private_comment — Comment on the project (in alphabetical order).

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

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Pool ID in ascending order.
            * created — Pool creation date.
            * last_started — The date the pool was last started (ascending).

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

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Training pool ID in ascending order.
            * created — Training pool creation date.
            * last_started — The date the pool was last started (ascending).

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

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Skill ID in ascending order.
            * created — Skill creation date.

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
        status: The status of an assigned task suite:
            * `ACTIVE` — Assigned but not completed.
            * `SUBMITTED` — Completed but not checked.
            * `ACCEPTED` — Accepted by the requester.
            * `REJECTED` — Rejected by the requester.
            * `SKIPPED` — Skipped by the Toloker.
            * `EXPIRED` — Time for completing tasks has expired.
        task_id: The ID of a task. The task suite containing that task, matches this search criteria.
        task_suite_id: The ID of a task suite.
        pool_id: Task suites in the pool with the specified ID.
        user_id: Task suites assigned to the Toloker with the specified ID.
        id_lt: Task suites with assignment IDs less than the specified value.
        id_lte: Task suites with assignment IDs less than or equal to the specified value.
        id_gt: Task suites with assignment IDs greater than the specified value.
        id_gte: Task suites with assignment IDs greater than or equal to the specified value.
        created_lt: Task suites assigned before the specified date.
        created_lte: Task suites assigned before or on the specified date.
        created_gt: Task suites assigned after the specified date.
        created_gte: Task suites assigned after or on the specified date.
        submitted_lt: Task suites completed before the specified date.
        submitted_lte: Task suites completed before or on the specified date.
        submitted_gt: Task suites completed after the specified date.
        submitted_gte: Task suites completed after or on the specified date.
        accepted_lt: Task suites accepted before the specified date.
        accepted_lte: Task suites accepted before or on the specified date.
        accepted_gt: Task suites accepted after the specified date.
        accepted_gte: Task suites accepted after or on the specified date.
        rejected_lt: Task suites rejected before the specified date.
        rejected_lte: Task suites rejected before or on the specified date.
        rejected_gt: Task suites rejected after the specified date.
        rejected_gte: Task suites rejected after or on the specified date.
        skipped_lt: Task suites skipped before the specified date.
        skipped_lte: Task suites skipped before or on the specified date.
        skipped_gt: Task suites skipped after the specified date.
        skipped_gte: Task suites skipped after or on the specified date.
        expired_lt: Task suites expired before the specified date.
        expired_lte: Task suites expired before or on the specified date.
        expired_gt: Task suites expired after the specified date.
        expired_gte: Task suites expired after or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime
        submitted: datetime.datetime
        accepted: datetime.datetime
        rejected: datetime.datetime
        skipped: datetime.datetime
        expired: datetime.datetime

    def _list_converter(value: Union[str, Assignment.Status, List[Union[str, Assignment.Status]]]):
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
    'AssignmentSortItems', ['id', 'created', 'submitted', 'accepted', 'rejected', 'skipped', 'expired'],
    # docstring
    """Parameters for sorting assignment search results

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — ID for issuing a set of tasks.
            * created — Date of issue of the set of tasks.
            * submitted — Date of completion of the set of tasks.
            * accepted — Date the set of tasks was accepted.
            * rejected — Date the set of tasks was rejected.
            * skipped — Date the set of tasks was skipped.
            * expired — Date the set of tasks was expired.

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.AssignmentSortItems(['-submitted', 'id'])
        >>> result = toloka_client.find_assignments(status='SUBMITTED', sort=sort, limit=10)
        ...
    """
)


class AggregatedSolutionSearchRequest(BaseSearchRequest):
    """Parameters for filtering aggregated responses.

    Attributes:
        task_id_lt: Tasks with an ID less than the specified value.
        task_id_lte: Tasks with an ID less than or equal to the specified value.
        task_id_gt: Tasks with an ID greater than the specified value.
        task_id_gte: Tasks with an ID greater than or equal to the specified value.
    """

    class CompareFields:
        task_id: str


AggregatedSolutionSortItems = BaseSortItems.for_fields(
    'AggregatedSolutionSortItems', ['task_id'],
    # docstring
    """Parameters for sorting aggregated solution search results.

    To sort in descending order add a hyphen before the parameter. For example, `sort=-task_id`.

    Attributes:
        items: Possible values:
            * `task_id` — Sort by a task ID in ascending order.
    """
)


class TaskSearchRequest(BaseSearchRequest):
    """Parameters for searching tasks

    Attributes:
        pool_id: The ID of the pool to get tasks from.
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
        overlap_lte: Tasks with an overlap less than or equal to the specified value.
        overlap_gt: Tasks with an overlap greater than the specified value.
        overlap_gte: Tasks with an overlap greater than or equal to the specified value.
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

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Job ID (in ascending order).
            * created — Date of creation of the task.

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

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Task set ID (in ascending order).
            * created — Date of creation of the set of tasks.

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
        type: Attachment type. Currently the key can have only one value — ASSIGNMENT_ATTACHMENT.
        user_id: ID of the Toloker who uploaded the file(s).
        assignment_id: Assignment ID.
        pool_id: Pool ID.
        owner_id: Optional[str]
        owner_company_id: Optional[str]
        id_lt: Files with an ID less than the specified value.
        id_lte: Files with an ID less than or equal to the specified value.
        id_gt: Files with an ID greater than the specified value.
        id_gte: Files with an ID greater than or equal to the specified value.
        created_lt: Files uploaded by Tolokers before the specified date.
        created_lte: Files uploaded by Tolokers before or on the specified date.
        created_gt: Files uploaded by Tolokers after the specified date.
        created_gte: Files uploaded by Tolokers after or on the specified date.
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

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — File ID in ascending order.
            * created — Date of sending the file.

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.AttachmentSortItems(['-created', 'id'])
        >>> result = toloka_client.find_attachments(pool_id=my_pretty_pool_id, sort=sort, limit=10)
        ...
    """
)


class UserSkillSearchRequest(BaseSearchRequest):
    """Parameters for searching Toloker skill

    Attributes:
        user_id: Toloker's ID.
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

    user_id: str
    skill_id: str


UserSkillSortItems = BaseSortItems.for_fields(
    'UserSkillSortItems', ['id', 'created', 'modified'],
    # docstring
    """Parameters for sorting Toloker skill search results

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Skill ID in ascending order.
            * created — Date the skill was created.
            * modified — Date the skill was modified.

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.UserSkillSortItems(['-created', 'id'])
        >>> result = toloka_client.find_user_skills(skill_id=my_useful_skill_id, sort=sort, limit=10)
        ...
    """
)


class UserRestrictionSearchRequest(BaseSearchRequest):
    """Parameters for searching Toloker restriction

    Attributes:
        scope: The scope of the ban
            * ALL_PROJECTS
            * PROJECT
            * POOL
        user_id: Toloker's ID.
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
    """Parameters for sorting Toloker restriction search results

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Restriction IDs.
            * created — Creation date.

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.UserRestrictionSortItems(['-created', 'id'])
        >>> result = toloka_client.find_user_restrictions(pool_id=my_pretty_pool_id, sort=sort, limit=10)
        ...
    """
)


class UserBonusSearchRequest(BaseSearchRequest):
    """Parameters for searching `UserBonus` instances.

    Attributes:
        user_id: The ID of the Toloker.
        assignment_id: The ID of the Toloker's response to the task a reward is issued for.
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
    assignment_id: str
    private_comment: str


UserBonusSortItems = BaseSortItems.for_fields(
    'UserBonusSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting `UserBonus` search results

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Bonus ID in ascending order.
            * created — Creation date (ascending).

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

    def _list_converter(value: Union[str, Folder, List[Union[str, Folder]]]) -> List[Folder]:
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

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Thread ID in ascending order.
            * created — Creation date (ascending).
    """
)


class WebhookSubscriptionSearchRequest(BaseSearchRequest):
    """Parameters for searching webhook-subscriptions.

    Attributes:
        event_type: Event type.
        pool_id: ID of the pool for which subscription information is requested.
        id_lt: Subscriptions with an ID less than the specified value.
        id_lte: Subscriptions with an ID less than or equal to the specified value.
        id_gt: Subscriptions with an ID greater than the specified value.
        id_gte: Subscriptions with an ID greater than or equal to the specified value.
        created_lt: Subscriptions created before the specified date.
        created_lte: Subscriptions created before or on the specified date.
        created_gt: Subscriptions created after the specified date.
        created_gte: Subscriptions created after or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime

    event_type: WebhookSubscription.EventType
    pool_id: str


WebhookSubscriptionSortItems = BaseSortItems.for_fields(
    'WebhookSubscriptionSortItems', ['id', 'created'],
    # docstring
    """Parameters for sorting webhook-subscriptions search results

    Attributes:
        items: Fields by which to sort. Possible values:
            * id — Subscription ID (in ascending order).
            * created — Date of creation of the subscription.

    Example:
        How to specify and use SortItems.

        >>> sort = toloka.client.search_requests.WebhookSubscriptionSortItems(['-created', 'id'])
        >>> result = toloka_client.find_webhook_subscriptions(event_type=some_event_type, pool_id=my_pretty_pool_id, sort=sort, limit=10)
        ...
    """
)


class AppProjectSearchRequest(BaseSearchRequest):
    """Parameters for searching App projects.

    Attributes:
        app_id: Projects created using the solution with the specified ID.
        parent_app_project_id: Projects cloned from the project with the specified ID. Projects can be cloned in the web version of Toloka.
        status: Projects with the specified status.
        after_id: The ID of a project used for cursor pagination.
        scope: Values:
            * `MY` — Projects created by you.
            * `COMPANY` — Projects created by requesters from your company.
            * `REQUESTER_LIST` — Projects created by requesters in the `requester_ids` list.
        requester_ids: A list with requester IDs separated by a comma. Use the list with parameter `scope = REQUESTER_LIST`.
        id_gt: Projects with IDs greater than the specified value.
        id_gte: Projects with IDs greater than or equal to the specified value.
        id_lt: Projects with IDs less than the specified value.
        id_lte: Projects with IDs less than or equal to the specified value.
        name_gt: Projects with a name lexicographically greater than the specified value.
        name_gte: Projects with a name lexicographically greater than or equal to the specified value.
        name_lt: Projects with a name lexicographically less than the specified value.
        name_lte: Projects with a name lexicographically less than or equal to the specified value.
        created_gt: Projects created after the specified date.
        created_gte: Projects created after or on the specified date.
        created_lt: Projects created before the specified date.
        created_lte: Projects created before or on the specified date.
    """

    @unique
    class Scope(Enum):
        MY = 'MY'
        COMPANY = 'COMPANY'
        REQUESTER_LIST = 'REQUESTER_LIST'

    class CompareFields:
        id: str
        name: str
        created: datetime.datetime

    def _list_converter(value: Union[str, List[str]]):
        if isinstance(value, str):
            value = value.split(',')
            value = [item.strip() for item in value]
        return value

    def _list_setter(self, attribute, value):
        return AppProjectSearchRequest._list_converter(value)

    app_id: str
    parent_app_project_id: str
    status: AppProject.Status
    after_id: str
    scope: Scope
    requester_ids: List[str] = attr.attrib(converter=_list_converter, on_setattr=_list_setter)


AppProjectSortItems = BaseSortItems.for_fields(
    'AppProjectSortItems', ['id', 'name', 'created'],
    # docstring
    """Keys for sorting App projects in search results.

    Attributes:
        key: The sorting key. Supported keys:
            * `id` — An App project ID.
            * `name` — An App project name.
            * `created` — A project creation date.
    """
)


class AppSearchRequest(BaseSearchRequest):
    """Parameters for searching App solutions.

    Attributes:
        after_id: The ID of a solution used for cursor pagination.
        lang: ISO 639 language code.
        id_gt: Solutions with IDs greater than the specified value.
        id_gte: Solutions with IDs greater than or equal to the specified value.
        id_lt: Solutions with IDs less than the specified value.
        id_lte: Solutions with IDs less than or equal to the specified value.
        name_gt: Solutions with names lexicographically greater than the specified value.
        name_gte: Solutions with names lexicographically greater than or equal to the specified value.
        name_lt: Solutions with names lexicographically less than the specified value.
        name_lte: Solutions with names lexicographically less than or equal to the specified value.
    """

    class CompareFields:
        id: str

    after_id: str
    lang: str


AppSortItems = BaseSortItems.for_fields(
    'AppSortItems', ['id'],
    # docstring
    """Keys for sorting App solutions in search results.

    Attributes:
        key: The sorting key. Supported keys:
            * `id` — An App solution ID.
    """
)


class AppItemSearchRequest(BaseSearchRequest):
    """Parameters for searching App task items.

    Attributes:
        after_id: The ID of the item used for cursor pagination.
        batch_id: The ID of the batch to look in.
        status: Items with the specified status.
        id_gt: Items with IDs greater than the specified value.
        id_gte: Items with IDs greater than or equal to the specified value.
        id_lt: Items with IDs less than the specified value.
        id_lte: Items with IDs less than or equal to the specified value.
        created_gt: Items created after the specified date.
        created_gte: Items created after or on the specified date.
        created_lt: Items created before the specified date.
        created_lte: Items created before or on the specified date.
        finished_gt: Items labeled after the specified date.
        finished_gte: Items labeled after or on the specified date.
        finished_lt: Items labeled before the specified date.
        finished_lte: Items labeled before or on the specified date.
    """

    class CompareFields:
        id: str
        created: datetime.datetime
        finished: datetime.datetime

    after_id: str
    batch_id: str
    status: AppItem.Status


AppItemSortItems = BaseSortItems.for_fields(
    'AppItemSortItems', ['id', 'created', 'finished', 'status'],
    # docstring
    """Keys for sorting App task items in search results.

    Attributes:
        key: The sorting key. Supported keys:
            * `id` — A task item ID.
            * `created` — The date and time when the item was created.
            * `finished` — The date and time when the item processing was completed.
            * `status` — The item status.
    """
)


class AppBatchSearchRequest(BaseSearchRequest):
    """Parameters for searching batches in an App project.

    Attributes:
        after_id: The ID of the batch used for cursor pagination.
        status: Batches with the specified status.
        id_gt: Batches with IDs greater than the specified value.
        id_gte: Batches with IDs greater than or equal to the specified value.
        id_lt: Batches with IDs less than the specified value.
        id_lte: Batches with IDs less than or equal to the specified value.
        name_gt: Batches with names lexicographically greater than the specified value.
        name_gte: Batches with names lexicographically greater than or equal to the specified value.
        name_lt: Batches with names lexicographically less than the specified value.
        name_lte: Batches with names lexicographically less than or equal to the specified value.
        created_gt: Batches created after the specified date.
        created_gte: Batches created after or on the specified date.
        created_lt: Batches created before the specified date.
        created_lte: Batches created before or on the specified date.
    """

    class CompareFields:
        id: str
        name: str
        created: datetime.datetime

    after_id: str
    status: AppBatch.Status


AppBatchSortItems = BaseSortItems.for_fields(
    'AppBatchSortItems', ['id', 'name', 'created', 'status'],
    # docstring
    """Keys for sorting App batches in search results.

    Attributes:
        key: The sorting key. Supported keys:
            * `id` — A batch ID.
            * `name` — A batch name.
            * `created` — A batch creation date.
            * `status` — The item status.
    """
)
