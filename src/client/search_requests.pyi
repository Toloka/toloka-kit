from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar

from .assignment import Assignment
from .attachment import Attachment
from .message_thread import Folder
from .pool import Pool
from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass
from .project import Project
from .training import Training
from .user_restriction import UserRestriction


SortItemSelf = TypeVar('SortItemSelf', bound='BaseSortItem')
SortItemsSelf = TypeVar('SortItemsSelf', bound='BaseSortItems')

class SortOrder(Enum):
    ...

class BaseSortItem(BaseTolokaObject):

    def unstructure(self): ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self) -> None: ...

    _unexpected: Optional[Dict[str, Any]]

class BaseSortItems(BaseTolokaObject):

    def unstructure(self): ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self) -> None: ...

    _unexpected: Optional[Dict[str, Any]]

class SearchRequestMetaclass(BaseTolokaObjectMetaclass):
    ...

class BaseSearchRequest(BaseTolokaObject):
    """Base class for all search request classes
    """
    ...

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

    class CompareFields(object):

        id: str
        created: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        status: Optional[Project.ProjectStatus] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...
    ) -> None: ...

    status: Optional[Project.ProjectStatus]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]

class ProjectSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime
        last_started: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        status: Optional[Pool.Status] = ...,
        project_id: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...,
        last_started_lt: Optional[datetime] = ...,
        last_started_lte: Optional[datetime] = ...,
        last_started_gt: Optional[datetime] = ...,
        last_started_gte: Optional[datetime] = ...
    ) -> None: ...

    status: Optional[Pool.Status]
    project_id: Optional[str]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]
    last_started_lt: Optional[datetime]
    last_started_lte: Optional[datetime]
    last_started_gt: Optional[datetime]
    last_started_gte: Optional[datetime]

class PoolSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime
        last_started: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        status: Optional[Training.Status] = ...,
        project_id: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...,
        last_started_lt: Optional[datetime] = ...,
        last_started_lte: Optional[datetime] = ...,
        last_started_gt: Optional[datetime] = ...,
        last_started_gte: Optional[datetime] = ...
    ) -> None: ...

    status: Optional[Training.Status]
    project_id: Optional[str]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]
    last_started_lt: Optional[datetime]
    last_started_lte: Optional[datetime]
    last_started_gt: Optional[datetime]
    last_started_gte: Optional[datetime]

class TrainingSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        name: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...
    ) -> None: ...

    name: Optional[str]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]

class SkillSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime
        submitted: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        status: Optional[Assignment.Status] = ...,
        task_id: Optional[str] = ...,
        task_suite_id: Optional[str] = ...,
        pool_id: Optional[str] = ...,
        user_id: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...,
        submitted_lt: Optional[datetime] = ...,
        submitted_lte: Optional[datetime] = ...,
        submitted_gt: Optional[datetime] = ...,
        submitted_gte: Optional[datetime] = ...
    ) -> None: ...

    def _list_converter(value): ...

    def _list_setter(self, attribute, value): ...

    def unstructure(self) -> Optional[dict]: ...

    status: Optional[Assignment.Status]
    task_id: Optional[str]
    task_suite_id: Optional[str]
    pool_id: Optional[str]
    user_id: Optional[str]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]
    submitted_lt: Optional[datetime]
    submitted_lte: Optional[datetime]
    submitted_gt: Optional[datetime]
    submitted_gte: Optional[datetime]

class AssignmentSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

class AggregatedSolutionSearchRequest(BaseSearchRequest):
    """Parameters for searching aggregated solution

    Attributes:
        task_id_lt: Jobs with an ID greater than the specified value.
        task_id_lte: Jobs with an ID greater than or equal to the specified value.
        task_id_gt: Jobs with an ID less than the specified value.
        task_id_gte: Jobs with an ID less than or equal to the specified value.
    """

    class CompareFields(object):

        task_id: str

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        task_id_lt: Optional[str] = ...,
        task_id_lte: Optional[str] = ...,
        task_id_gt: Optional[str] = ...,
        task_id_gte: Optional[str] = ...
    ) -> None: ...

    task_id_lt: Optional[str]
    task_id_lte: Optional[str]
    task_id_gt: Optional[str]
    task_id_gte: Optional[str]

class AggregatedSolutionSortItems(BaseSortItems):
    """Parameters for sorting aggregated solution search results

    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * task_id - In ascending order.
    """

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime
        overlap: int

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        pool_id: Optional[str] = ...,
        overlap: Optional[int] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...,
        overlap_lt: Optional[int] = ...,
        overlap_lte: Optional[int] = ...,
        overlap_gt: Optional[int] = ...,
        overlap_gte: Optional[int] = ...
    ) -> None: ...

    pool_id: Optional[str]
    overlap: Optional[int]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]
    overlap_lt: Optional[int]
    overlap_lte: Optional[int]
    overlap_gt: Optional[int]
    overlap_gte: Optional[int]

class TaskSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime
        overlap: int

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        task_id: Optional[str] = ...,
        pool_id: Optional[str] = ...,
        overlap: Optional[int] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...,
        overlap_lt: Optional[int] = ...,
        overlap_lte: Optional[int] = ...,
        overlap_gt: Optional[int] = ...,
        overlap_gte: Optional[int] = ...
    ) -> None: ...

    task_id: Optional[str]
    pool_id: Optional[str]
    overlap: Optional[int]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]
    overlap_lt: Optional[int]
    overlap_lte: Optional[int]
    overlap_gt: Optional[int]
    overlap_gte: Optional[int]

class TaskSuiteSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        name: Optional[str] = ...,
        type: Optional[Attachment.Type] = ...,
        user_id: Optional[str] = ...,
        assignment_id: Optional[str] = ...,
        pool_id: Optional[str] = ...,
        owner_id: Optional[str] = ...,
        owner_company_id: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...
    ) -> None: ...

    name: Optional[str]
    type: Optional[Attachment.Type]
    user_id: Optional[str]
    assignment_id: Optional[str]
    pool_id: Optional[str]
    owner_id: Optional[str]
    owner_company_id: Optional[str]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]

class AttachmentSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime
        modified: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        name: Optional[str] = ...,
        user_id: Optional[str] = ...,
        skill_id: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...,
        modified_lt: Optional[datetime] = ...,
        modified_lte: Optional[datetime] = ...,
        modified_gt: Optional[datetime] = ...,
        modified_gte: Optional[datetime] = ...
    ) -> None: ...

    name: Optional[str]
    user_id: Optional[str]
    skill_id: Optional[str]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]
    modified_lt: Optional[datetime]
    modified_lte: Optional[datetime]
    modified_gt: Optional[datetime]
    modified_gte: Optional[datetime]

class UserSkillSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        scope: Optional[UserRestriction.Scope] = ...,
        user_id: Optional[str] = ...,
        project_id: Optional[str] = ...,
        pool_id: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...
    ) -> None: ...

    scope: Optional[UserRestriction.Scope]
    user_id: Optional[str]
    project_id: Optional[str]
    pool_id: Optional[str]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]

class UserRestrictionSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        user_id: Optional[str] = ...,
        private_comment: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...
    ) -> None: ...

    user_id: Optional[str]
    private_comment: Optional[str]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]

class UserBonusSortItems(BaseSortItems):
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

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]

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

    class CompareFields(object):

        id: str
        created: datetime

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        folder: Optional[Folder] = ...,
        folder_ne: Optional[Folder] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...
    ) -> None: ...

    def _list_converter(value): ...

    def _list_setter(self, attribute, value): ...

    def unstructure(self) -> Optional[dict]: ...

    folder: Optional[Folder]
    folder_ne: Optional[Folder]
    id_lt: Optional[str]
    id_lte: Optional[str]
    id_gt: Optional[str]
    id_gte: Optional[str]
    created_lt: Optional[datetime]
    created_lte: Optional[datetime]
    created_gt: Optional[datetime]
    created_gte: Optional[datetime]

class MessageThreadSortItems(BaseSortItems):
    """Parameters for sorting message thread search results

    You can specify multiple parameters.
    To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

    Attributes:
        items: Fields by which to sort. Possible values:
            * id - Thread ID in ascending order.
            * created - Creation date in UTC format yyyy-MM-DD (ascending).
    """

    class SortItem(BaseSortItem):

        class SortField(Enum):
            ...


        _unexpected: Optional[Dict[str, Any]]
        field: Optional[SortField]
        order: Optional[SortOrder]


    _unexpected: Optional[Dict[str, Any]]
    items: Optional[List[SortItem]]
