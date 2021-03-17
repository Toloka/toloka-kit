from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from pandas.core.frame import DataFrame
from typing import (
    BinaryIO,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Union,
    overload
)
from urllib3.util.retry import Retry # type: ignore
from uuid import UUID

from .aggregation import (
    AggregatedSolution,
    AggregatedSolutionType,
    PoolAggregatedSolutionRequest,
    WeightedDynamicOverlapTaskAggregatedSolutionRequest
)
from .analytics_request import AnalyticsRequest
from .assignment import (
    Assignment,
    AssignmentPatch,
    GetAssignmentsTsvParameters
)
from .attachment import Attachment
from .batch_create_results import (
    TaskBatchCreateResult,
    TaskSuiteBatchCreateResult,
    UserBonusBatchCreateResult
)
from .clone_results import CloneResults
from .filter import FilterCondition
from .message_thread import (
    Folder,
    MessageThread,
    MessageThreadCompose,
    MessageThreadFolders,
    MessageThreadReply,
    RecipientsSelectType
)
from .operation_log import OperationLogItem
from .operations import (
    AggregatedSolutionOperation,
    Operation,
    PoolArchiveOperation,
    PoolCloneOperation,
    PoolCloseOperation,
    PoolOpenOperation,
    ProjectArchiveOperation,
    TaskSuiteCreateBatchOperation,
    TasksCreateOperation,
    TrainingArchiveOperation,
    TrainingCloneOperation,
    TrainingCloseOperation,
    TrainingOpenOperation,
    UserBonusCreateBatchOperation
)
from .pool import Pool, PoolPatchRequest
from .project import Project
from .requester import Requester
from .search_requests import (
    AggregatedSolutionSearchRequest,
    AggregatedSolutionSortItems,
    AssignmentSearchRequest,
    AssignmentSortItems,
    AttachmentSearchRequest,
    AttachmentSortItems,
    MessageThreadSearchRequest,
    MessageThreadSortItems,
    PoolSearchRequest,
    PoolSortItems,
    ProjectSearchRequest,
    ProjectSortItems,
    SkillSearchRequest,
    SkillSortItems,
    TaskSearchRequest,
    TaskSortItems,
    TaskSuiteSearchRequest,
    TaskSuiteSortItems,
    TrainingSearchRequest,
    TrainingSortItems,
    UserBonusSearchRequest,
    UserBonusSortItems,
    UserRestrictionSearchRequest,
    UserRestrictionSortItems,
    UserSkillSearchRequest,
    UserSkillSortItems
)
from .search_results import (
    AggregatedSolutionSearchResult,
    AssignmentSearchResult,
    AttachmentSearchResult,
    MessageThreadSearchResult,
    PoolSearchResult,
    ProjectSearchResult,
    SkillSearchResult,
    TaskSearchResult,
    TaskSuiteSearchResult,
    TrainingSearchResult,
    UserBonusSearchResult,
    UserRestrictionSearchResult,
    UserSkillSearchResult
)
from .skill import Skill
from .task import (
    CreateTaskParameters,
    CreateTasksParameters,
    Task,
    TaskOverlapPatch,
    TaskPatch
)
from .task_suite import (
    TaskSuite,
    TaskSuiteCreateRequestParameters,
    TaskSuiteOverlapPatch,
    TaskSuitePatch
)
from .training import Training
from .user_bonus import UserBonus, UserBonusCreateRequestParameters
from .user_restriction import UserRestriction
from .user_skill import SetUserSkillRequest, UserSkill


class TolokaClient(object):

    class Environment(Enum):
        ...

    def __init__(
        self,
        token: str,
        environment: Union[Environment, str],
        retries: Union[int, Retry] = ...,
        timeout: Union[float, Tuple[float, float]] = ...
    ): ...

    @overload
    def aggregate_solutions_by_pool(
        self,*,
        type: Optional[AggregatedSolutionType] = ...,
        pool_id: Optional[str] = ...,
        answer_weight_skill_id: Optional[str] = ...,
        fields: Optional[List[PoolAggregatedSolutionRequest.Field]] = ...
    ) -> AggregatedSolutionOperation:
        """Aggregate responses in a pool

        """
        ...

    @overload
    def aggregate_solutions_by_pool(
        self,
        request: PoolAggregatedSolutionRequest
    ) -> AggregatedSolutionOperation:
        """Aggregate responses in a pool

        """
        ...

    @overload
    def aggregate_solutions_by_task(
        self,*,
        task_id: Optional[str] = ...,
        pool_id: Optional[str] = ...,
        answer_weight_skill_id: Optional[str] = ...,
        fields: Optional[List[WeightedDynamicOverlapTaskAggregatedSolutionRequest.Field]] = ...
    ) -> AggregatedSolution:
        """Aggregate responses to a single task

        """
        ...

    @overload
    def aggregate_solutions_by_task(
        self,
        request: WeightedDynamicOverlapTaskAggregatedSolutionRequest
    ) -> AggregatedSolution:
        """Aggregate responses to a single task

        """
        ...

    @overload
    def find_aggregated_solutions(
        self,
        operation_id: str,
        task_id_lt: Optional[str] = ...,
        task_id_lte: Optional[str] = ...,
        task_id_gt: Optional[str] = ...,
        task_id_gte: Optional[str] = ...,
        sort: Union[List[str], AggregatedSolutionSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> AggregatedSolutionSearchResult:
        """Finds aggregated solutions

        """
        ...

    @overload
    def find_aggregated_solutions(
        self,
        operation_id: str,
        request: AggregatedSolutionSearchRequest,
        sort: Union[List[str], AggregatedSolutionSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> AggregatedSolutionSearchResult:
        """Finds aggregated solutions

        """
        ...

    def accept_assignment(
        self,
        assignment_id: str,
        public_comment: str
    ) -> Assignment:
        """Accept response: change SUBMITTED to ACCEPTED.

        """
        ...

    @overload
    def find_assignments(
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
        submitted_gte: Optional[datetime] = ...,
        sort: Union[List[str], AssignmentSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> AssignmentSearchResult:
        """Finds assignments

        """
        ...

    @overload
    def find_assignments(
        self,
        request: AssignmentSearchRequest,
        sort: Union[List[str], AssignmentSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> AssignmentSearchResult:
        """Finds assignments

        """
        ...

    def get_assignment(self, assignment_id: str) -> Assignment:
        """Gets assignment by assignment_id

        """
        ...

    @overload
    def get_assignments(
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
    ) -> Generator[Assignment, None, None]:
        """Finds assignments

        """
        ...

    @overload
    def get_assignments(
        self,
        request: AssignmentSearchRequest
    ) -> Generator[Assignment, None, None]:
        """Finds assignments

        """
        ...

    @overload
    def patch_assignment(
        self,
        assignment_id: str,*,
        public_comment: Optional[str] = ...,
        status: Optional[Assignment.Status] = ...
    ) -> Assignment:
        """Patches assignment with patch

        """
        ...

    @overload
    def patch_assignment(
        self,
        assignment_id: str,
        patch: AssignmentPatch
    ) -> Assignment:
        """Patches assignment with patch

        """
        ...

    def reject_assignment(
        self,
        assignment_id: str,
        public_comment: str
    ) -> Assignment:
        """Reject response: change SUBMITTED to REJECTED.

        """
        ...

    @overload
    def find_attachments(
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
        created_gte: Optional[datetime] = ...,
        sort: Union[List[str], AttachmentSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> AttachmentSearchResult:
        """Finds attachments

        """
        ...

    @overload
    def find_attachments(
        self,
        request: AttachmentSearchRequest,
        sort: Union[List[str], AttachmentSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> AttachmentSearchResult:
        """Finds attachments

        """
        ...

    def get_attachment(self, attachment_id: str) -> Attachment:
        """Gets attachment metadata without downloading it

        """
        ...

    @overload
    def get_attachments(
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
    ) -> Generator[Attachment, None, None]:
        """Finds attachments

        Unlike find_attachments, returns generator. Does not sort attachments.
        """
        ...

    @overload
    def get_attachments(
        self,
        request: AttachmentSearchRequest
    ) -> Generator[Attachment, None, None]:
        """Finds attachments

        Unlike find_attachments, returns generator. Does not sort attachments.
        """
        ...

    def download_attachment(self, attachment_id: str, out: BinaryIO) -> None:
        """Downloads attachment

        """
        ...

    def add_message_thread_to_folders(
        self,
        message_thread_id: str,
        folders: Union[List[Folder], MessageThreadFolders]
    ) -> MessageThread:
        """Add a message thread to one or more folders

        """
        ...

    @overload
    def compose_message_thread(
        self,*,
        recipients_select_type: Optional[RecipientsSelectType] = ...,
        topic: Optional[Dict[str, str]] = ...,
        text: Optional[Dict[str, str]] = ...,
        answerable: Optional[bool] = ...,
        recipients_ids: Optional[List[str]] = ...,
        recipients_filter: Optional[FilterCondition] = ...
    ) -> MessageThread:
        """Sends message to users

        The sent message is added to a new message thread.
        """
        ...

    @overload
    def compose_message_thread(
        self,
        compose: MessageThreadCompose
    ) -> MessageThread:
        """Sends message to users

        The sent message is added to a new message thread.
        """
        ...

    @overload
    def find_message_threads(
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
        created_gte: Optional[datetime] = ...,
        sort: Union[List[str], MessageThreadSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> MessageThreadSearchResult:
        """Finds message threads satisfying filters

        """
        ...

    @overload
    def find_message_threads(
        self,
        request: MessageThreadSearchRequest,
        sort: Union[List[str], MessageThreadSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> MessageThreadSearchResult:
        """Finds message threads satisfying filters

        """
        ...

    def reply_message_thread(
        self,
        message_thread_id: str,
        reply: MessageThreadReply
    ) -> MessageThread:
        """Reply to message thread

        """
        ...

    @overload
    def get_message_threads(
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
    ) -> Generator[MessageThread, None, None]:
        """Finds message threads satisfying filters

        """
        ...

    @overload
    def get_message_threads(
        self,
        request: MessageThreadSearchRequest
    ) -> Generator[MessageThread, None, None]:
        """Finds message threads satisfying filters

        """
        ...

    def remove_message_thread_from_folders(
        self,
        message_thread_id: str,
        folders: Union[List[Folder], MessageThreadFolders]
    ) -> MessageThread:
        """Removes a message thread from one or more folders

        """
        ...

    def archive_project(self, project_id: str) -> Project:
        """Archive a project

        If a project isn't being used, you can send it to the archive.
        """
        ...

    def archive_project_async(self, project_id: str) -> ProjectArchiveOperation: ...

    def create_project(self, project: Project) -> Project:
        """Create a project

        """
        ...

    @overload
    def find_projects(
        self,
        status: Optional[Project.ProjectStatus] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...,
        sort: Union[List[str], ProjectSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> ProjectSearchResult:
        """Finds projects

        """
        ...

    @overload
    def find_projects(
        self,
        request: ProjectSearchRequest,
        sort: Union[List[str], ProjectSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> ProjectSearchResult:
        """Finds projects

        """
        ...

    def get_project(self, project_id: str) -> Project:
        """Gets properties of a project.

        Using this method on TRAINING pools is deprecated.
        """
        ...

    @overload
    def get_projects(
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
    ) -> Generator[Project, None, None]:
        """Finds projects

        """
        ...

    @overload
    def get_projects(
        self,
        request: ProjectSearchRequest
    ) -> Generator[Project, None, None]:
        """Finds projects

        """
        ...

    def update_project(self, project_id: str, project: Project) -> Project:
        """Makes changes to a project.

        Using this method on TRAINING pools is deprecated.
        """
        ...

    def clone_project(
        self,
        project_id: str,
        reuse_controllers: bool = ...
    ) -> CloneResults:
        """Synchronously clones the project, all pools and trainings

        Emulates cloning behaviour via Toloka interface:
        - the same skills will be used
        - the same quality control collectors will be used (could be changed by reuse_controllers=False)
        - the expiration date will not be changed in the new project
        - etc.        

        Doesn't have transaction - can clone project, and then raise on cloning pool.
        Doesn't copy tasks/golden tasks/training tasks.

        Args:
            project_id: ID of the project to be cloned.
            reuse_quality_controllers: Use same quality controllers in cloned and created projects. Defaults to True.
                This means that all quality control rules will be applied to both projects.
                For example, if you have rule "fast_submitted_count", fast responses counts across both projects.

        Returns:
            Tuple[Project, List[Pool], List[Training]]: All created objects project, pools and trainings.

        Example:

            >>> project, pools, trainings = toloka_client.clone_project('123')
            >>> # add tasks in pools and trainings
            ...
        """
        ...

    def archive_pool(self, pool_id: str) -> Pool:
        """Moves a pool to the archive.

        If a pool isn't in use, it can be moved to the archive. The pool must have the "closed" status.
        Using this method on TRAINING pools is deprecated.
        """
        ...

    def archive_pool_async(self, pool_id: str) -> PoolArchiveOperation: ...

    def close_pool(self, pool_id: str) -> Pool:
        """Closes a pool.

        Using this method on TRAINING pools is deprecated.
        """
        ...

    def close_pool_async(self, pool_id: str) -> PoolCloseOperation: ...

    def close_pool_for_update(self, pool_id: str) -> Pool:
        """Using this method on TRAINING pools is deprecated.

        """
        ...

    def close_pool_for_update_async(self, pool_id: str) -> PoolCloseOperation: ...

    def clone_pool(self, pool_id: str) -> Pool:
        """Clones a pool.

        To create a duplicate pool, clone it. An empty pool will be created with the same parameters.
        Using this method on TRAINING pools is deprecated.
        """
        ...

    def clone_pool_async(self, pool_id: str) -> PoolCloneOperation: ...

    def create_pool(self, pool: Pool) -> Pool:
        """Creates a REGULAR pool

        You can send a maximum of 20 requests of this kind per minute and 100 requests per day.
        Training pool creation is available only in the web interface.
        """
        ...

    @overload
    def find_pools(
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
        last_started_gte: Optional[datetime] = ...,
        sort: Union[List[str], PoolSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> PoolSearchResult:
        """Finds REGULAR pools.

        """
        ...

    @overload
    def find_pools(
        self,
        request: PoolSearchRequest,
        sort: Union[List[str], PoolSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> PoolSearchResult:
        """Finds REGULAR pools.

        """
        ...

    def get_pool(self, pool_id: str) -> Pool:
        """Gets properties of a pool.

        Using this method on TRAINING pools is deprecated.
        """
        ...

    @overload
    def get_pools(
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
    ) -> Generator[Pool, None, None]:
        """Finds REGULAR pools.

        """
        ...

    @overload
    def get_pools(
        self,
        request: PoolSearchRequest
    ) -> Generator[Pool, None, None]:
        """Finds REGULAR pools.

        """
        ...

    def open_pool(self, pool_id: str) -> Pool:
        """Opens a pool.

        To make tasks available to users, you need to open the pool.
        Using this method on TRAINING pools is deprecated.
        """
        ...

    def open_pool_async(self, pool_id: str) -> PoolOpenOperation: ...

    @overload
    def patch_pool(self, pool_id: str, priority: Optional[int] = ...) -> Pool:
        """Using this method on TRAINING pools is deprecated.

        """
        ...

    @overload
    def patch_pool(self, pool_id: str, request: PoolPatchRequest) -> Pool:
        """Using this method on TRAINING pools is deprecated.

        """
        ...

    def update_pool(self, pool_id: str, pool: Pool) -> Pool:
        """Edits a REGULAR pool.

        You can only edit a training pool via the web interface.
        """
        ...

    def archive_training(self, training_id: str) -> Training: ...

    def archive_training_async(self, training_id: str) -> TrainingArchiveOperation: ...

    def close_training(self, training_id: str) -> Training: ...

    def close_training_async(self, training_id: str) -> TrainingCloseOperation: ...

    def clone_training(self, training_id: str) -> Training: ...

    def clone_training_async(self, training_id: str) -> TrainingCloneOperation: ...

    def create_training(self, training: Training) -> Training: ...

    @overload
    def find_trainings(
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
        last_started_gte: Optional[datetime] = ...,
        sort: Union[List[str], TrainingSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> TrainingSearchResult: ...

    @overload
    def find_trainings(
        self,
        request: TrainingSearchRequest,
        sort: Union[List[str], TrainingSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> TrainingSearchResult: ...

    def get_training(self, training_id: str) -> Training: ...

    @overload
    def get_trainings(
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
    ) -> Generator[Training, None, None]: ...

    @overload
    def get_trainings(
        self,
        request: TrainingSearchRequest
    ) -> Generator[Training, None, None]: ...

    def open_training(self, training_id: str) -> Training: ...

    def open_training_async(self, training_id: str) -> TrainingOpenOperation: ...

    def update_training(self, training_id: str, training: Training) -> Training: ...

    @overload
    def create_skill(
        self,*,
        name: Optional[str] = ...,
        private_comment: Optional[str] = ...,
        hidden: Optional[bool] = ...,
        skill_ttl_hours: Optional[int] = ...,
        training: Optional[bool] = ...,
        public_name: Optional[Dict[str, str]] = ...,
        public_requester_description: Optional[Dict[str, str]] = ...,
        id: Optional[str] = ...,
        created: Optional[datetime] = ...
    ) -> Skill:
        """Creates a skill

        You can send a maximum of 10 requests of this kind per minute and 100 requests per day.
        """
        ...

    @overload
    def create_skill(self, skill: Skill) -> Skill:
        """Creates a skill

        You can send a maximum of 10 requests of this kind per minute and 100 requests per day.
        """
        ...

    @overload
    def find_skills(
        self,
        name: Optional[str] = ...,
        id_lt: Optional[str] = ...,
        id_lte: Optional[str] = ...,
        id_gt: Optional[str] = ...,
        id_gte: Optional[str] = ...,
        created_lt: Optional[datetime] = ...,
        created_lte: Optional[datetime] = ...,
        created_gt: Optional[datetime] = ...,
        created_gte: Optional[datetime] = ...,
        sort: Union[List[str], SkillSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> SkillSearchResult:
        """Finds skills

        """
        ...

    @overload
    def find_skills(
        self,
        request: SkillSearchRequest,
        sort: Union[List[str], SkillSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> SkillSearchResult:
        """Finds skills

        """
        ...

    def get_skill(self, skill_id: str) -> Skill:
        """Finds skills

        """
        ...

    @overload
    def get_skills(
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
    ) -> Generator[Skill, None, None]:
        """Finds skills

        """
        ...

    @overload
    def get_skills(
        self,
        request: SkillSearchRequest
    ) -> Generator[Skill, None, None]:
        """Finds skills

        """
        ...

    def update_skill(self, skill_id: str, skill: Skill):
        """Edits a skill

        """
        ...

    def get_analytics(self, stats: List[AnalyticsRequest]) -> Operation: ...

    @overload
    def create_task(
        self,
        task: Task,*,
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...
    ) -> Task:
        """Creates a task

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        """
        ...

    @overload
    def create_task(
        self,
        task: Task,
        parameters: Optional[CreateTaskParameters] = ...
    ) -> Task:
        """Creates a task

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        """
        ...

    @overload
    def create_tasks(
        self,
        tasks: List[Task],*,
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...,
        skip_invalid_items: Optional[bool] = ...,
        operation_id: Optional[UUID] = ...,
        async_mode: Optional[bool] = ...
    ) -> TaskBatchCreateResult:
        """Creates multiple tasks

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        The response contains information about the created tasks.
        Maximum of 5000 task per request if async_mode is False.
        Recomended maximum of 10,000 task per request if async_mode is True.
        """
        ...

    @overload
    def create_tasks(
        self,
        tasks: List[Task],
        parameters: Optional[CreateTasksParameters] = ...
    ) -> TaskBatchCreateResult:
        """Creates multiple tasks

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        The response contains information about the created tasks.
        Maximum of 5000 task per request if async_mode is False.
        Recomended maximum of 10,000 task per request if async_mode is True.
        """
        ...

    @overload
    def create_tasks_async(
        self,
        tasks: List[Task],*,
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...,
        skip_invalid_items: Optional[bool] = ...,
        operation_id: Optional[UUID] = ...,
        async_mode: Optional[bool] = ...
    ) -> TasksCreateOperation:
        """Creates multiple tasks

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

        Creates an asynchronous operation that runs in the background. The response contains information about the
        operation (start and completion time, status, number of task suites).
        Recomended maximum of 10,000 task per request if async_mode is True.
        It's recomended to use 'create_tasks' method with async_mode is True.
        """
        ...

    @overload
    def create_tasks_async(
        self,
        tasks: List[Task],
        parameters: Optional[CreateTasksParameters] = ...
    ) -> TasksCreateOperation:
        """Creates multiple tasks

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

        Creates an asynchronous operation that runs in the background. The response contains information about the
        operation (start and completion time, status, number of task suites).
        Recomended maximum of 10,000 task per request if async_mode is True.
        It's recomended to use 'create_tasks' method with async_mode is True.
        """
        ...

    @overload
    def find_tasks(
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
        overlap_gte: Optional[int] = ...,
        sort: Union[List[str], TaskSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> TaskSearchResult:
        """Finds tasks

        """
        ...

    @overload
    def find_tasks(
        self,
        request: TaskSearchRequest,
        sort: Union[List[str], TaskSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> TaskSearchResult:
        """Finds tasks

        """
        ...

    def get_task(self, task_id: str) -> Task:
        """Gets a task

        """
        ...

    @overload
    def get_tasks(
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
    ) -> Generator[Task, None, None]:
        """Finds tasks

        """
        ...

    @overload
    def get_tasks(
        self,
        request: TaskSearchRequest
    ) -> Generator[Task, None, None]:
        """Finds tasks

        """
        ...

    @overload
    def patch_task(
        self,
        task_id: str,*,
        overlap: Optional[int] = ...,
        infinite_overlap: Optional[bool] = ...,
        baseline_solutions: Optional[List[Task.BaselineSolution]] = ...
    ) -> Task:
        """Edit a task

        """
        ...

    @overload
    def patch_task(self, task_id: str, patch: TaskPatch) -> Task:
        """Edit a task

        """
        ...

    @overload
    def patch_task_overlap_or_min(
        self,
        task_id: str,*,
        overlap: Optional[int] = ...,
        infinite_overlap: Optional[bool] = ...
    ) -> Task:
        """Changes the task overlap

        If provided overlap can't be set, minimal possible will be set instead.
        """
        ...

    @overload
    def patch_task_overlap_or_min(
        self,
        task_id: str,
        patch: TaskOverlapPatch
    ) -> Task:
        """Changes the task overlap

        If provided overlap can't be set, minimal possible will be set instead.
        """
        ...

    @overload
    def create_task_suite(
        self,
        task_suite: TaskSuite,*,
        operation_id: Optional[UUID] = ...,
        skip_invalid_items: Optional[bool] = ...,
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...,
        async_mode: Optional[bool] = ...
    ) -> TaskSuite:
        """Creates a task suite

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        """
        ...

    @overload
    def create_task_suite(
        self,
        task_suite: TaskSuite,
        parameters: Optional[TaskSuiteCreateRequestParameters] = ...
    ) -> TaskSuite:
        """Creates a task suite

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        """
        ...

    @overload
    def create_task_suites(
        self,
        task_suites: List[TaskSuite],*,
        operation_id: Optional[UUID] = ...,
        skip_invalid_items: Optional[bool] = ...,
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...,
        async_mode: Optional[bool] = ...
    ) -> TaskSuiteBatchCreateResult:
        """Creates multiple task suites

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Maximum of 5000 task suites per request if async_mode is False.
        Recomended maximum of 10,000 task suites per request if async_mode is True.
        """
        ...

    @overload
    def create_task_suites(
        self,
        task_suites: List[TaskSuite],
        parameters: Optional[TaskSuiteCreateRequestParameters] = ...
    ) -> TaskSuiteBatchCreateResult:
        """Creates multiple task suites

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Maximum of 5000 task suites per request if async_mode is False.
        Recomended maximum of 10,000 task suites per request if async_mode is True.
        """
        ...

    @overload
    def create_task_suites_async(
        self,
        task_suites: List[TaskSuite],*,
        operation_id: Optional[UUID] = ...,
        skip_invalid_items: Optional[bool] = ...,
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...,
        async_mode: Optional[bool] = ...
    ) -> TaskSuiteCreateBatchOperation:
        """Creates multiple task suites

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Recomended maximum of 10,000 task suites per request if async_mode is True.
        """
        ...

    @overload
    def create_task_suites_async(
        self,
        task_suites: List[TaskSuite],
        parameters: Optional[TaskSuiteCreateRequestParameters] = ...
    ) -> TaskSuiteCreateBatchOperation:
        """Creates multiple task suites

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Recomended maximum of 10,000 task suites per request if async_mode is True.
        """
        ...

    @overload
    def find_task_suites(
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
        overlap_gte: Optional[int] = ...,
        sort: Union[List[str], TaskSuiteSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> TaskSuiteSearchResult:
        """Finds task suites

        """
        ...

    @overload
    def find_task_suites(
        self,
        request: TaskSuiteSearchRequest,
        sort: Union[List[str], TaskSuiteSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> TaskSuiteSearchResult:
        """Finds task suites

        """
        ...

    def get_task_suite(self, task_suite_id: str) -> TaskSuite:
        """Gets task suite

        """
        ...

    @overload
    def get_task_suites(
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
    ) -> Generator[TaskSuite, None, None]:
        """Finds task suites

        """
        ...

    @overload
    def get_task_suites(
        self,
        request: TaskSuiteSearchRequest
    ) -> Generator[TaskSuite, None, None]:
        """Finds task suites

        """
        ...

    @overload
    def patch_task_suite(
        self,
        task_suite_id: str,*,
        infinite_overlap=...,
        overlap=...,
        issuing_order_override: Optional[float] = ...,
        open_pool: Optional[bool] = ...
    ) -> TaskSuite:
        """Edit a task suite by applying a patch

        """
        ...

    @overload
    def patch_task_suite(
        self,
        task_suite_id: str,
        patch: TaskSuitePatch
    ) -> TaskSuite:
        """Edit a task suite by applying a patch

        """
        ...

    @overload
    def patch_task_suite_overlap_or_min(
        self,
        task_suite_id: str,*,
        overlap: Optional[int] = ...
    ) -> TaskSuite:
        """Changes the task suite overlap

        If provided overlap can't be set, minimal possible will be set instead.
        """
        ...

    @overload
    def patch_task_suite_overlap_or_min(
        self,
        task_suite_id: str,
        patch: TaskSuiteOverlapPatch
    ) -> TaskSuite:
        """Changes the task suite overlap

        If provided overlap can't be set, minimal possible will be set instead.
        """
        ...

    def get_operation(self, operation_id: str) -> Operation:
        """Get operation

        """
        ...

    def wait_operation(
        self,
        op: Operation,
        timeout: timedelta = ...
    ) -> Operation:
        """Waits for the operation to complete

        """
        ...

    def get_operation_log(self, operation_id: str) -> List[OperationLogItem]: ...

    def create_user_bonus(
        self,
        user_bonus: UserBonus,
        parameters: Optional[UserBonusCreateRequestParameters] = ...
    ) -> UserBonus: ...

    @overload
    def create_user_bonuses(
        self,
        user_bonuses: List[UserBonus],*,
        operation_id: Optional[str] = ...,
        skip_invalid_items: Optional[bool] = ...
    ) -> UserBonusBatchCreateResult:
        """Awards bonuses to users

        You can send a maximum of 10,000 requests of this kind per day.
        Synchronous. The response contains information about bonuses awarded. Maximum of 100 bonuses per request.
        """
        ...

    @overload
    def create_user_bonuses(
        self,
        user_bonuses: List[UserBonus],
        parameters: Optional[UserBonusCreateRequestParameters] = ...
    ) -> UserBonusBatchCreateResult:
        """Awards bonuses to users

        You can send a maximum of 10,000 requests of this kind per day.
        Synchronous. The response contains information about bonuses awarded. Maximum of 100 bonuses per request.
        """
        ...

    @overload
    def create_user_bonuses_async(
        self,
        user_bonuses: List[UserBonus],*,
        operation_id: Optional[str] = ...,
        skip_invalid_items: Optional[bool] = ...
    ) -> UserBonusCreateBatchOperation:
        """Awards bonuses to users

        You can send a maximum of 10,000 requests of this kind per day.
        Asynchronous. Creates an asynchronous operation that runs in the background.
        The response contains information about the operation.
        """
        ...

    @overload
    def create_user_bonuses_async(
        self,
        user_bonuses: List[UserBonus],
        parameters: Optional[UserBonusCreateRequestParameters] = ...
    ) -> UserBonusCreateBatchOperation:
        """Awards bonuses to users

        You can send a maximum of 10,000 requests of this kind per day.
        Asynchronous. Creates an asynchronous operation that runs in the background.
        The response contains information about the operation.
        """
        ...

    @overload
    def find_user_bonuses(
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
        created_gte: Optional[datetime] = ...,
        sort: Union[List[str], UserBonusSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> UserBonusSearchResult:
        """Finds bonuses awarded to the user

        """
        ...

    @overload
    def find_user_bonuses(
        self,
        request: UserBonusSearchRequest,
        sort: Union[List[str], UserBonusSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> UserBonusSearchResult:
        """Finds bonuses awarded to the user

        """
        ...

    def get_user_bonus(self, user_bonus_id: str) -> UserBonus:
        """Finds bonuses awarded to the user

        """
        ...

    @overload
    def get_user_bonuses(
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
    ) -> Generator[UserBonus, None, None]:
        """Finds bonuses awarded to the user

        """
        ...

    @overload
    def get_user_bonuses(
        self,
        request: UserBonusSearchRequest
    ) -> Generator[UserBonus, None, None]:
        """Finds bonuses awarded to the user

        """
        ...

    @overload
    def find_user_restrictions(
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
        created_gte: Optional[datetime] = ...,
        sort: Union[List[str], UserRestrictionSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> UserRestrictionSearchResult:
        """Finds user bans

        """
        ...

    @overload
    def find_user_restrictions(
        self,
        request: UserRestrictionSearchRequest,
        sort: Union[List[str], UserRestrictionSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> UserRestrictionSearchResult:
        """Finds user bans

        """
        ...

    def get_user_restriction(self, user_restriction_id: str) -> UserRestriction:
        """Gets information about the ban

        """
        ...

    @overload
    def get_user_restrictions(
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
    ) -> Generator[UserRestriction, None, None]:
        """Finds user bans

        """
        ...

    @overload
    def get_user_restrictions(
        self,
        request: UserRestrictionSearchRequest
    ) -> Generator[UserRestriction, None, None]:
        """Finds user bans

        """
        ...

    def set_user_restriction(
        self,
        user_restriction: UserRestriction
    ) -> UserRestriction:
        """Blocks a user from accessing tasks

        """
        ...

    def delete_user_restriction(self, user_restriction_id: str) -> None:
        """Unblocks access to tasks

        """
        ...

    def get_requester(self) -> Requester: ...

    @overload
    def find_user_skills(
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
        modified_gte: Optional[datetime] = ...,
        sort: Union[List[str], UserSkillSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> UserSkillSearchResult:
        """Finds the user's skills

        """
        ...

    @overload
    def find_user_skills(
        self,
        request: UserSkillSearchRequest,
        sort: Union[List[str], UserSkillSortItems, None] = ...,
        limit: Optional[int] = ...
    ) -> UserSkillSearchResult:
        """Finds the user's skills

        """
        ...

    def get_user_skill(self, user_skill_id: str) -> UserSkill:
        """Gets the user's skill value

        """
        ...

    @overload
    def get_user_skills(
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
    ) -> Generator[UserSkill, None, None]:
        """Finds the user's skills

        """
        ...

    @overload
    def get_user_skills(
        self,
        request: UserSkillSearchRequest
    ) -> Generator[UserSkill, None, None]:
        """Finds the user's skills

        """
        ...

    @overload
    def set_user_skill(
        self,*,
        skill_id: Optional[str] = ...,
        user_id: Optional[str] = ...,
        value: Optional[Decimal] = ...
    ) -> UserSkill:
        """Sets the skill value for a user

        """
        ...

    @overload
    def set_user_skill(self, request: SetUserSkillRequest) -> UserSkill:
        """Sets the skill value for a user

        """
        ...

    def delete_user_skill(self, user_skill_id: str) -> None:
        """Removes a skill for a user

        """
        ...

    @overload
    def get_assignments_df(
        self,
        pool_id: str,*,
        status: Optional[List[GetAssignmentsTsvParameters.Status]] = ...,
        start_time_from: Optional[datetime] = ...,
        start_time_to: Optional[datetime] = ...,
        exclude_banned: Optional[bool] = ...,
        field: Optional[List[GetAssignmentsTsvParameters.Field]] = ...
    ) -> DataFrame:
        """Download assignments as pandas.DataFrame

        """
        ...

    @overload
    def get_assignments_df(
        self,
        pool_id: str,
        parameters: GetAssignmentsTsvParameters
    ) -> DataFrame:
        """Download assignments as pandas.DataFrame

        """
        ...
