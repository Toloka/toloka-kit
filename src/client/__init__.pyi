__all__ = [
    'actions',
    'aggregation',
    'analytics_request',
    'assignment',
    'attachment',
    'batch_create_results',
    'clone_results',
    'collectors',
    'conditions',
    'error_codes',
    'exceptions',
    'filter',
    'message_thread',
    'operation_log',
    'operations',
    'owner',
    'quality_control',
    'requester',
    'search_requests',
    'search_results',
    'skill',
    'solution',
    'task',
    'task_distribution_function',
    'task_suite',
    'training',
    'user_bonus',
    'user_restriction',
    'user_skill',
    'webhook_subscription',
    'TolokaClient',
    'Assignment',
    'Attachment',
    'Folder',
    'MessageThread',
    'MessageThreadReply',
    'MessageThreadFolders',
    'MessageThreadCompose',
    'Skill',
    'TaskSuite',
    'Task',
    'Training',
    'UserBonus',
    'Pool',
    'Project',
]
import toloka.client.actions
import toloka.client.aggregation
import toloka.client.analytics_request
import toloka.client.assignment
import toloka.client.attachment
import toloka.client.batch_create_results
import toloka.client.clone_results
import toloka.client.collectors
import toloka.client.conditions
import toloka.client.error_codes
import toloka.client.exceptions
import toloka.client.filter
import toloka.client.message_thread
import toloka.client.operation_log
import toloka.client.operations
import toloka.client.owner
import toloka.client.quality_control
import toloka.client.requester
import toloka.client.search_requests
import toloka.client.search_results
import toloka.client.skill
import toloka.client.solution
import toloka.client.task
import toloka.client.task_distribution_function
import toloka.client.task_suite
import toloka.client.training
import toloka.client.user_bonus
import toloka.client.user_restriction
import toloka.client.user_skill
import toloka.client.webhook_subscription

from datetime import (
    datetime,
    timedelta
)
from decimal import Decimal
from enum import Enum
from pandas.core.frame import DataFrame
from requests.packages.urllib3.util.retry import Retry
from toloka.client.aggregation import (
    AggregatedSolution,
    AggregatedSolutionType,
    PoolAggregatedSolutionRequest,
    WeightedDynamicOverlapTaskAggregatedSolutionRequest
)
from toloka.client.analytics_request import AnalyticsRequest
from toloka.client.assignment import (
    Assignment,
    AssignmentPatch,
    GetAssignmentsTsvParameters
)
from toloka.client.attachment import Attachment
from toloka.client.batch_create_results import (
    TaskBatchCreateResult,
    TaskSuiteBatchCreateResult,
    UserBonusBatchCreateResult,
    WebhookSubscriptionBatchCreateResult
)
from toloka.client.clone_results import CloneResults
from toloka.client.filter import FilterCondition
from toloka.client.message_thread import (
    Folder,
    MessageThread,
    MessageThreadCompose,
    MessageThreadFolders,
    MessageThreadReply,
    RecipientsSelectType
)
from toloka.client.operation_log import OperationLogItem
from toloka.client.operations import (
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
from toloka.client.pool import (
    Pool,
    PoolPatchRequest
)
from toloka.client.project import Project
from toloka.client.requester import Requester
from toloka.client.search_requests import (
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
    UserSkillSortItems,
    WebhookSubscriptionSearchRequest,
    WebhookSubscriptionSortItems
)
from toloka.client.search_results import (
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
    UserSkillSearchResult,
    WebhookSubscriptionSearchResult
)
from toloka.client.skill import Skill
from toloka.client.task import (
    CreateTaskParameters,
    CreateTasksParameters,
    Task,
    TaskOverlapPatch,
    TaskPatch
)
from toloka.client.task_suite import (
    TaskSuite,
    TaskSuiteCreateRequestParameters,
    TaskSuiteOverlapPatch,
    TaskSuitePatch
)
from toloka.client.training import Training
from toloka.client.user_bonus import (
    UserBonus,
    UserBonusCreateRequestParameters
)
from toloka.client.user_restriction import UserRestriction
from toloka.client.user_skill import (
    SetUserSkillRequest,
    UserSkill
)
from toloka.client.webhook_subscription import WebhookSubscription
from typing import (
    BinaryIO,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Union,
    overload
)
from uuid import UUID

class TolokaClient:
    """Implements interaction with the Toloka API

    All other objects are created or modified only in the memory of your computer.
    Only by calling one of the TolokaClient methods, you can transfer information from these objects to Toloka.
    For Example. If you create an instance of Project, it will not create such a project in Toloka. You need to call the
    TolokaClient.create_project method and pass the project instance there.
    Likewise. If you read the project using the TolokaClient.get_project method, you will get an instance of Project.
    But if you change something in this object, it will not affect the existing project in Toloka. To apply these changes,
    call TolokaClient.update_project and pass the changed Project there.

    Args:
        token: You OAuth token for Toloka. You can learn more about how to get it here: https://yandex.ru/dev/toloka/doc/concepts/access.html?lang=en
        environment: There are two versions of Toloka. You need to register separately in each of them:
            * SANDBOX: Testing version oif Toloka. You can test complex projects before the start. Nobody saw your tasks.
            * PRODUCTION: Production version of Toloka for requesters. You spend money and get result.
        retries: Retry policy. You can use the following types:
            * int - The number of retries for all requests. In this case, the retry policy is created automatically.
            * Retry - Deprecated. Use retryer_factory instead. Fully specified retry policy that will apply to all requests.
        timeout: Same as timeout in Requests. The connect timeout is the number of seconds Requests will wait for your client
            to establish a connection to a remote machine call on the socket.
            * If you specify a single value for the timeout, it will be applied to both the connect and the read timeouts.
            * Specify a tuple if you would like to set the values separately.
            * Set the timeout value to None if you're willing to wait forever.
        url: If you want to set a specific URL for some reason, for example, for testing.
            You can only set one parameter, "url" or "environment", not both.
        retry_quotas: List of quotas that must be retried. By default retries only minutes quotas. None or empty list for not retrying quotas.
            You must set this parameter to None, then you specify the 'retries' parameter as Retry instance.
            You can specify quotas:
            * MIN - Retry minutes quotas.
            * HOUR - Retry hourly quotas. This is means that the program just sleeps for an hour! Be careful.
            * DAY - Retry daily quotas. We strongly not recommended retrying these quotas.
        retryer_factory: Factory that creates Retry object.

    Example:
        How to create TolokaClient instance and make your first request to Toloka.

        >>> your_oauth_token = input('Enter your token:')
        >>> toloka_client = toloka.TolokaClient(your_oauth_token, 'PRODUCTION')  # Or switch to 'SANDBOX' environment
        ...

        **Note**: `toloka_client` instance will be used to pass all API calls later on.
    """

    class Environment(Enum):
        """An enumeration.
        """

        SANDBOX = 'https://sandbox.toloka.yandex.com'
        PRODUCTION = 'https://toloka.yandex.com'

    def __init__(
        self,
        token: str,
        environment: Union[Environment, str, None] = None,
        retries: Union[int, Retry] = 3,
        timeout: Union[float, Tuple[float, float]] = ...,
        url: Optional[str] = None,
        retry_quotas: Union[List[str], str, None] = 'MIN',
        retryer_factory: Optional[Callable[[], Retry]] = None,
    ): ...

    def accept_assignment(
        self,
        assignment_id: str,
        public_comment: str
    ) -> Assignment:
        """Marks one assignment as accepted

        Used then your pool created with auto_accept_solutions=False parametr.

        Args:
            assignment_id: What assignment will be accepted.
            public_comment: Message to the performer.

        Returns:
            Assignment: Object with new status.

        Example:
            How to accept one assignment.

            >>> toloka_client.accept_assignment(assignment_id, 'Well done!')
            ...
        """
        ...

    def add_message_thread_to_folders(
        self,
        message_thread_id: str,
        folders: Union[List[Folder], MessageThreadFolders]
    ) -> MessageThread:
        """Adds a message chain to one or more folders ("unread", "important" etc.)

        Args:
            message_thread_id: ID of message chain.
            folders: List of folders, where to move chain.

        Returns:
            MessageThread: Full object by ID with updated folders.

        Example:
            >>> toloka_client.add_message_thread_to_folders(message_thread_id='1', folders=['IMPORTANT'])
            ...
        """
        ...

    @overload
    def aggregate_solutions_by_pool(self, request: PoolAggregatedSolutionRequest) -> AggregatedSolutionOperation:
        """Starts aggregation of solutions in the pool

        Responses to all completed tasks will be aggregated.
        The method only starts the aggregation and returns the operation for further tracking.

        **Note**: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
        methods and can perform on your computers: https://github.com/Toloka/crowd-kit

        Args:
            request: Parameters describing in which pool to aggregate solutions and by what rules.

        Returns:
            operations.AggregatedSolutionOperation: An operation upon completion of which you can get the results of the aggregation.

        Example:
            How to start aggregating solutions by pool.

            >>> aggregation_operation = toloka_client.aggregate_solutions_by_pool(
            >>>         type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
            >>>         pool_id=some_existing_pool_id,   # Aggregate in this pool
            >>>         answer_weight_skill_id=some_skill_id,   # Aggregate by this skill
            >>>         fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]  # Aggregate this field
            >>>     )
            >>> aggregation_operation = toloka_client.wait_operation(aggregation_operation)
            >>> # Now you can call "find_aggregated_solutions"
            ...
        """
        ...

    @overload
    def aggregate_solutions_by_pool(
        self,
        *,
        type: Optional[AggregatedSolutionType] = None,
        pool_id: Optional[str] = None,
        answer_weight_skill_id: Optional[str] = None,
        fields: Optional[List[PoolAggregatedSolutionRequest.Field]] = None
    ) -> AggregatedSolutionOperation:
        """Starts aggregation of solutions in the pool

        Responses to all completed tasks will be aggregated.
        The method only starts the aggregation and returns the operation for further tracking.

        **Note**: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
        methods and can perform on your computers: https://github.com/Toloka/crowd-kit

        Args:
            request: Parameters describing in which pool to aggregate solutions and by what rules.

        Returns:
            operations.AggregatedSolutionOperation: An operation upon completion of which you can get the results of the aggregation.

        Example:
            How to start aggregating solutions by pool.

            >>> aggregation_operation = toloka_client.aggregate_solutions_by_pool(
            >>>         type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
            >>>         pool_id=some_existing_pool_id,   # Aggregate in this pool
            >>>         answer_weight_skill_id=some_skill_id,   # Aggregate by this skill
            >>>         fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]  # Aggregate this field
            >>>     )
            >>> aggregation_operation = toloka_client.wait_operation(aggregation_operation)
            >>> # Now you can call "find_aggregated_solutions"
            ...
        """
        ...

    @overload
    def aggregate_solutions_by_task(self, request: WeightedDynamicOverlapTaskAggregatedSolutionRequest) -> AggregatedSolution:
        """Starts aggregation of solutions to a single task

        The method only starts the aggregation and returns the operation for further tracking.

        Args:
            request: Parameters describing on which task to aggregate solutions and by what rules.

        Returns:
            AggregatedSolution: Result of aggregation. Also contains input parameters and result confidence.

        Example:
            How to aggregate solutions to a task.

            >>> aggregation_operation = toloka_client.aggregate_solutions_by_task(
            >>>         type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
            >>>         pool_id=some_existing_pool_id,   # Task in this pool
            >>>         task_id=some_existing_task_id,   # Aggregate on this task
            >>>         answer_weight_skill_id=some_skill_id,   # Aggregate by this skill
            >>>         fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]  # Aggregate this field
            >>>     )
            >>> print(aggregation_operation.output_values['result'])
            ...
        """
        ...

    @overload
    def aggregate_solutions_by_task(
        self,
        *,
        task_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        answer_weight_skill_id: Optional[str] = None,
        fields: Optional[List[WeightedDynamicOverlapTaskAggregatedSolutionRequest.Field]] = None
    ) -> AggregatedSolution:
        """Starts aggregation of solutions to a single task

        The method only starts the aggregation and returns the operation for further tracking.

        Args:
            request: Parameters describing on which task to aggregate solutions and by what rules.

        Returns:
            AggregatedSolution: Result of aggregation. Also contains input parameters and result confidence.

        Example:
            How to aggregate solutions to a task.

            >>> aggregation_operation = toloka_client.aggregate_solutions_by_task(
            >>>         type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
            >>>         pool_id=some_existing_pool_id,   # Task in this pool
            >>>         task_id=some_existing_task_id,   # Aggregate on this task
            >>>         answer_weight_skill_id=some_skill_id,   # Aggregate by this skill
            >>>         fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]  # Aggregate this field
            >>>     )
            >>> print(aggregation_operation.output_values['result'])
            ...
        """
        ...

    def archive_pool(self, pool_id: str) -> Pool:
        """Sends pool to archive

        The pool must be in the status "closed".
        The archived pool is not deleted. You can access it when you will need it.

        Args:
            pool_id: ID of pool that will be archived.

        Returns:
            Pool: Object with updated status.

        Example:
            >>> closed_pool = next(toloka_client.get_pools(status='CLOSED'))
            >>> toloka_client.archive_pool(pool_id=closed_pool.id)
            ...
        """
        ...

    def archive_pool_async(self, pool_id: str) -> PoolArchiveOperation:
        """Sends pool to archive, asynchronous version

        The pool must be in the status "closed".
        The archived pool is not deleted. You can access it when you will need it.

        Args:
            pool_id: ID of pool that will be archived.

        Returns:
            PoolArchiveOperation: An operation upon completion of which you can get the pool with updated status.

        Example:
            >>> closed_pool = next(toloka_client.get_pools(status='CLOSED'))
            >>> archive_op = toloka_client.archive_pool_async(pool_id=closed_pool.id)
            >>> toloka_client.wait_operation(archive_op)
            ...
        """
        ...

    def archive_project(self, project_id: str) -> Project:
        """Sends project to archive

        Use it when you have no need this project anymore. To perform the operation, all pools in the project must be archived.
        The archived project is not deleted. You can access it when you will need it.

        Args:
            project_id: ID of project that will be archived.

        Returns:
            Project: Object with updated status.

        Example:
            >>> toloka_client.archive_project(project_id='1')
            ...
        """
        ...

    def archive_project_async(self, project_id: str) -> ProjectArchiveOperation:
        """Sends project to archive, asynchronous version

        Use when you have no need this project anymore. To perform the operation, all pools in the project must be archived.
        The archived project is not deleted. You can access it when you will need it.

        Args:
            project_id: ID of project that will be archived.

        Returns:
            ProjectArchiveOperation: An operation upon completion of which you can get the project with updated status.

        Example:
            >>> archive_op = toloka_client.archive_project_async(project_id='1')
            >>> toloka_client.wait_operation(archive_op)
            ...
        """
        ...

    def archive_training(self, training_id: str) -> Training:
        """Sends training to archive

        The training must be in the status "closed".
        The archived training is not deleted. You can access it when you will need it.

        Args:
            training_id: ID of training that will be archived.

        Returns:
            Training: Object with updated status.

        Example:
            >>> closed_training = next(toloka_client.get_trainings(status='CLOSED'))
            >>> toloka_client.archive_training(training_id=closed_training.id)
            ...
        """
        ...

    def archive_training_async(self, training_id: str) -> TrainingArchiveOperation:
        """Sends training to archive, asynchronous version

        The training must be in the status "closed".
        The archived training is not deleted. You can access it when you will need it.

        Args:
            training_id: ID of training that will be archived.

        Returns:
            TrainingArchiveOperation: An operation upon completion of which you can get the training with updated status.

        Example:
            >>> closed_training = next(toloka_client.find_trainings(status='CLOSED'))
            >>> archive_op = toloka_client.archive_training_async(training_id=closed_training.id)
            >>> toloka_client.wait_operation(archive_op)
            ...
        """
        ...

    def clone_pool(self, pool_id: str) -> Pool:
        """Duplicates existing pool

        An empty pool with the same parameters will be created.
        A new pool will be attached to the same project.

        Args:
            pool_id: ID of the existing pool.

        Returns:
            Pool: New pool.

        Example:
            >>> toloka_client.clone_pool(pool_id='1')
            ...
        """
        ...

    def clone_pool_async(self, pool_id: str) -> PoolCloneOperation:
        """Duplicates existing pool, asynchronous version

        An empty pool with the same parameters will be created.
        A new pool will be attached to the same project.

        Args:
            pool_id: ID of the existing pool.

        Returns:
            PoolCloneOperation: An operation upon completion of which you can get the new pool.

        Example:
            >>> new_pool = toloka_client.clone_pool_async(pool_id='1')
            >>> toloka_client.wait_operation(new_pool)
            ...
        """
        ...

    def clone_project(
        self,
        project_id: str,
        reuse_controllers: bool = True
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
            reuse_controllers: Use same quality controllers in cloned and created projects. Defaults to True.
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

    def clone_training(self, training_id: str) -> Training:
        """Duplicates existing training

        An empty training with the same parameters will be created.
        A new training will be attached to the same project.

        Args:
            training_id: ID of the existing training.

        Returns:
            Training: New training.

        Example:
            >>> toloka_client.clone_training(training_id='1')
            ...
        """
        ...

    def clone_training_async(self, training_id: str) -> TrainingCloneOperation:
        """Duplicates existing training, asynchronous version

        An empty training with the same parameters will be created.
        A new training will be attached to the same project.

        Args:
            training_id: ID of the existing training.

        Returns:
            TrainingCloneOperation: An operation upon completion of which you can get the new training.

        Example:
            >>> clone_training = toloka_client.clone_training_async(training_id='1')
            >>> toloka_client.wait_operation(clone_training)
            ...
        """
        ...

    def close_pool(self, pool_id: str) -> Pool:
        """Stops distributing tasks from the pool

        If all tasks done, the pool will be closed automatically.

        Args:
            pool_id: ID of the pool that will be closed.

        Returns:
            Pool: Pool object with new status.

        Example:
            >>> open_pool = next(toloka_client.get_pools(status='OPEN'))
            >>> toloka_client.close_pool(pool_id=open_pool.id)
            ...
        """
        ...

    def close_pool_async(self, pool_id: str) -> PoolCloseOperation:
        """Stops distributing tasks from the pool, asynchronous version

        If all tasks done, the pool will be closed automatically.

        Args:
            pool_id: ID of the pool that will be closed.

        Returns:
            PoolCloseOperation: An operation upon completion of which you can get the pool with updated status.

        Example:
            >>> open_pool = next(toloka_client.get_pools(status='OPEN'))
            >>> close_op = toloka_client.close_pool_async(pool_id=open_pool.id)
            >>> toloka_client.wait_operation(close_op)
            ...
        """
        ...

    def close_pool_for_update(self, pool_id: str) -> Pool:
        """Closes pool for update

        Example:
            >>> toloka_client.close_pool_for_update(pool_id='1')
            ...
        """
        ...

    def close_pool_for_update_async(self, pool_id: str) -> PoolCloseOperation:
        """Closes pool for update, asynchronous version

        Example:
            >>> close_op = toloka_client.close_pool_for_update_async(pool_id='1')
            >>> toloka_client.wait_operation(close_op)
            ...
        """
        ...

    def close_training(self, training_id: str) -> Training:
        """Stops distributing tasks from the training

        Args:
            training_id: ID of the training that will be closed.

        Returns:
            Training: Training object with new status.

        Example:
            >>> open_training = next(toloka_client.get_trainings(status='OPEN'))
            >>> toloka_client.close_training(training_id=open_training.id)
            ...
        """
        ...

    def close_training_async(self, training_id: str) -> TrainingCloseOperation:
        """Stops distributing tasks from the training, asynchronous version

        Args:
            training_id: ID of the training that will be closed.

        Returns:
            TrainingCloseOperation: An operation upon completion of which you can get the training with updated status.

        Example:
            >>> open_training = next(toloka_client.get_trainings(status='OPEN'))
            >>> close_training = toloka_client.close_training_async(training_id=open_training.id)
            >>> toloka_client.wait_operation(close_training)
            ...
        """
        ...

    @overload
    def compose_message_thread(self, compose: MessageThreadCompose) -> MessageThread:
        """Sends message to performer

        The sent message is added to a new message thread.

        Args:
            compose: Message parameters.

        Returns:
            MessageThread: New created thread.

        Example:
            If you want to thank Toloka performers who have tried to complete your tasks, send them a nice message.

            >>> message_text = 'Amazing job! We've just trained our first model with the data YOU prepared for us. Thank you!'
            >>> toloka_client.compose_message_thread(
            >>>     recipients_select_type='ALL',
            >>>     topic={'EN':'Thank you, performer!'},
            >>>     text={'EN': message_text},
            >>>     answerable=False
            >>> )
            ...
        """
        ...

    @overload
    def compose_message_thread(
        self,
        *,
        recipients_select_type: Optional[RecipientsSelectType] = None,
        topic: Optional[Dict[str, str]] = None,
        text: Optional[Dict[str, str]] = None,
        answerable: Optional[bool] = None,
        recipients_ids: Optional[List[str]] = None,
        recipients_filter: Optional[FilterCondition] = None
    ) -> MessageThread:
        """Sends message to performer

        The sent message is added to a new message thread.

        Args:
            compose: Message parameters.

        Returns:
            MessageThread: New created thread.

        Example:
            If you want to thank Toloka performers who have tried to complete your tasks, send them a nice message.

            >>> message_text = 'Amazing job! We've just trained our first model with the data YOU prepared for us. Thank you!'
            >>> toloka_client.compose_message_thread(
            >>>     recipients_select_type='ALL',
            >>>     topic={'EN':'Thank you, performer!'},
            >>>     text={'EN': message_text},
            >>>     answerable=False
            >>> )
            ...
        """
        ...

    def create_pool(self, pool: Pool) -> Pool:
        """Creates a new pool

        You can send a maximum of 20 requests of this kind per minute and 100 requests per day.

        Args:
            pool: New Pool with setted parameters.

        Returns:
            Pool: Created pool. With read-only fields.

        Example:
            How to create a new pool in a project.

            >>> new_pool = toloka.pool.Pool(
            >>>     project_id=existing_project_id,
            >>>     private_name='Pool 1',
            >>>     may_contain_adult_content=False,
            >>>     will_expire=datetime.datetime.utcnow() + datetime.timedelta(days=365),
            >>>     reward_per_assignment=0.01,
            >>>     assignment_max_duration_seconds=60*20,
            >>>     defaults=toloka.pool.Pool.Defaults(default_overlap_for_new_task_suites=3),
            >>>     filter=toloka.filter.Languages.in_('EN'),
            >>> )
            >>> new_pool.set_mixer_config(real_tasks_count=10, golden_tasks_count=0, training_tasks_count=0)
            >>> new_pool.quality_control.add_action(...)
            >>> new_pool = toloka_client.create_pool(new_pool)
            >>> print(new_pool.id)
            ...
        """
        ...

    def create_project(self, project: Project) -> Project:
        """Creates a new project

        Args:
            project: New Project with setted parameters.

        Returns:
            Project: Created project. With read-only fields.

        Example:
            How to create a new project.

            >>> new_project = toloka.project.Project(
            >>>     assignments_issuing_type=toloka.project.Project.AssignmentsIssuingType.AUTOMATED,
            >>>     public_name='My best project',
            >>>     public_description='Describe the picture',
            >>>     public_instructions='Describe in a few words what is happening in the image.',
            >>>     task_spec=toloka.project.task_spec.TaskSpec(
            >>>         input_spec={'image': toloka.project.field_spec.UrlSpec()},
            >>>         output_spec={'result': toloka.project.field_spec.StringSpec()},
            >>>         view_spec=project_interface,
            >>>     ),
            >>> )
            >>> new_project = toloka_client.create_project(new_project)
            >>> print(new_project.id)
            ...
        """
        ...

    @overload
    def create_skill(self, skill: Skill) -> Skill:
        """Creates a new Skill

        You can send a maximum of 10 requests of this kind per minute and 100 requests per day.

        Args:
            skill: New Skill with setted parameters.

        Returns:
            Skill: Created skill. With read-only fields.

        Example:
            How to create a new skill.

            >>> new_skill = toloka_client.create_skill(
            >>>     name='Area selection of road signs',
            >>>     public_requester_description={
            >>>         'EN': 'Performer is annotating road signs',
            >>>         'FR': 'L'exécuteur marque les signaux routier',
            >>>     },
            >>> )
            >>> print(new_skill.id)
            ...
        """
        ...

    @overload
    def create_skill(
        self,
        *,
        name: Optional[str] = None,
        private_comment: Optional[str] = None,
        hidden: Optional[bool] = None,
        skill_ttl_hours: Optional[int] = None,
        training: Optional[bool] = None,
        public_name: Optional[Dict[str, str]] = None,
        public_requester_description: Optional[Dict[str, str]] = None
    ) -> Skill:
        """Creates a new Skill

        You can send a maximum of 10 requests of this kind per minute and 100 requests per day.

        Args:
            skill: New Skill with setted parameters.

        Returns:
            Skill: Created skill. With read-only fields.

        Example:
            How to create a new skill.

            >>> new_skill = toloka_client.create_skill(
            >>>     name='Area selection of road signs',
            >>>     public_requester_description={
            >>>         'EN': 'Performer is annotating road signs',
            >>>         'FR': 'L'exécuteur marque les signaux routier',
            >>>     },
            >>> )
            >>> print(new_skill.id)
            ...
        """
        ...

    @overload
    def create_task(
        self,
        task: Task,
        parameters: Optional[CreateTaskParameters] = None
    ) -> Task:
        """Creates a new task

        It's better to use "create_tasks", if you need to insert several tasks.
        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

        Args:
            task: Task that need to be created.
            parameters: Parameters for Task creation controlling. Defaults to None.
                Allows you to use default overlap and start pool after task creation.

        Returns:
            Task: Created task.

        Example:
            >>> task = toloka.task.Task(
            >>>             input_values={'image': 'https://tlk.s3.yandex.net/dataset/cats_vs_dogs/dogs/048e5760fc5a46faa434922b2447a527.jpg'},
            >>>             pool_id='1')
            >>> toloka_client.create_task(task=task, allow_defaults=True)
            ...
        """
        ...

    @overload
    def create_task(
        self,
        task: Task,
        *,
        allow_defaults: Optional[bool] = None,
        open_pool: Optional[bool] = None
    ) -> Task:
        """Creates a new task

        It's better to use "create_tasks", if you need to insert several tasks.
        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

        Args:
            task: Task that need to be created.
            parameters: Parameters for Task creation controlling. Defaults to None.
                Allows you to use default overlap and start pool after task creation.

        Returns:
            Task: Created task.

        Example:
            >>> task = toloka.task.Task(
            >>>             input_values={'image': 'https://tlk.s3.yandex.net/dataset/cats_vs_dogs/dogs/048e5760fc5a46faa434922b2447a527.jpg'},
            >>>             pool_id='1')
            >>> toloka_client.create_task(task=task, allow_defaults=True)
            ...
        """
        ...

    @overload
    def create_task_suite(
        self,
        task_suite: TaskSuite,
        parameters: Optional[TaskSuiteCreateRequestParameters] = None
    ) -> TaskSuite:
        """Creates a new task suite

        Generally, you don't need to create a task set yourself, because you can create tasks and Toloka will create
        task suites for you. Use this method only then you need to group specific tasks in one suite or to set a
        different parameters on different tasks suites.
        It's better to use "create_task_suites", if you need to insert several task suites.
        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.

        Args:
            task_suite: Task suite that need to be created.
            parameters: Parameters for TaskSuite creation controlling. Defaults to None.

        Returns:
            TaskSuite: Created task suite.

        Example:
            >>> new_task_suite = toloka.task_suite.TaskSuite(
            >>>                 pool_id='1',
            >>>                 tasks=[toloka.task.Task(input_values={'label': 'Cats vs Dogs'})],
            >>>                 overlap=2)
            >>> toloka_client.create_task_suite(new_task_suite)
            ...
        """
        ...

    @overload
    def create_task_suite(
        self,
        task_suite: TaskSuite,
        *,
        operation_id: Optional[UUID] = None,
        skip_invalid_items: Optional[bool] = None,
        allow_defaults: Optional[bool] = None,
        open_pool: Optional[bool] = None,
        async_mode: Optional[bool] = True
    ) -> TaskSuite:
        """Creates a new task suite

        Generally, you don't need to create a task set yourself, because you can create tasks and Toloka will create
        task suites for you. Use this method only then you need to group specific tasks in one suite or to set a
        different parameters on different tasks suites.
        It's better to use "create_task_suites", if you need to insert several task suites.
        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.

        Args:
            task_suite: Task suite that need to be created.
            parameters: Parameters for TaskSuite creation controlling. Defaults to None.

        Returns:
            TaskSuite: Created task suite.

        Example:
            >>> new_task_suite = toloka.task_suite.TaskSuite(
            >>>                 pool_id='1',
            >>>                 tasks=[toloka.task.Task(input_values={'label': 'Cats vs Dogs'})],
            >>>                 overlap=2)
            >>> toloka_client.create_task_suite(new_task_suite)
            ...
        """
        ...

    @overload
    def create_task_suites(
        self,
        task_suites: List[TaskSuite],
        parameters: Optional[TaskSuiteCreateRequestParameters] = None
    ) -> TaskSuiteBatchCreateResult:
        """Creates many task suites in pools

        Generally, you don't need to create a task set yourself, because you can create tasks and Toloka will create
        task suites for you. Use this method only then you need to group specific tasks in one suite or to set a
        different parameters on different tasks suites.
        By default uses asynchronous operation inside. It's better not to set "async_mode=False", if you not understand
        clearly why you need it.
        Task suites can be from different pools. You can insert both regular tasks and golden-tasks.
        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Recomended maximum of 10,000 task suites per request if async_mode is True.

        Args:
            task_suites: List of task suites, that will be created.
            parameters: Parameters for TaskSuite creation controlling. Defaults to None, in which case the asynchronous
                operations is used.

        Returns:
            TaskSuiteBatchCreateResult: Result of task suites creating. Contains created task suites in `items` and
                problems in "validation_errors".

        Raises:
            ValidationApiError: If no tasks were created, or skip_invalid_items==False and there is a problem when
                checking any task.

        Example:
            >>> task_suites = [
            >>>     toloka.task_suite.TaskSuite(
            >>>         pool_id=pool.id,
            >>>         overlap=1,
            >>>         tasks=[
            >>>             toloka.task.Task(input_values={
            >>>                 'input1': some_input_value,
            >>>                 'input2': some_input_value
            >>>             })
            >>>         ]
            >>>     )
            >>> ]
            >>> task_suites = toloka_client.create_task_suites(task_suites)
            ...
        """
        ...

    @overload
    def create_task_suites(
        self,
        task_suites: List[TaskSuite],
        *,
        operation_id: Optional[UUID] = None,
        skip_invalid_items: Optional[bool] = None,
        allow_defaults: Optional[bool] = None,
        open_pool: Optional[bool] = None,
        async_mode: Optional[bool] = True
    ) -> TaskSuiteBatchCreateResult:
        """Creates many task suites in pools

        Generally, you don't need to create a task set yourself, because you can create tasks and Toloka will create
        task suites for you. Use this method only then you need to group specific tasks in one suite or to set a
        different parameters on different tasks suites.
        By default uses asynchronous operation inside. It's better not to set "async_mode=False", if you not understand
        clearly why you need it.
        Task suites can be from different pools. You can insert both regular tasks and golden-tasks.
        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Recomended maximum of 10,000 task suites per request if async_mode is True.

        Args:
            task_suites: List of task suites, that will be created.
            parameters: Parameters for TaskSuite creation controlling. Defaults to None, in which case the asynchronous
                operations is used.

        Returns:
            TaskSuiteBatchCreateResult: Result of task suites creating. Contains created task suites in `items` and
                problems in "validation_errors".

        Raises:
            ValidationApiError: If no tasks were created, or skip_invalid_items==False and there is a problem when
                checking any task.

        Example:
            >>> task_suites = [
            >>>     toloka.task_suite.TaskSuite(
            >>>         pool_id=pool.id,
            >>>         overlap=1,
            >>>         tasks=[
            >>>             toloka.task.Task(input_values={
            >>>                 'input1': some_input_value,
            >>>                 'input2': some_input_value
            >>>             })
            >>>         ]
            >>>     )
            >>> ]
            >>> task_suites = toloka_client.create_task_suites(task_suites)
            ...
        """
        ...

    @overload
    def create_task_suites_async(
        self,
        task_suites: List[TaskSuite],
        parameters: Optional[TaskSuiteCreateRequestParameters] = None
    ) -> TaskSuiteCreateBatchOperation:
        """Creates many task suites in pools, asynchronous version

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Recomended maximum of 10,000 task suites per request.

        Args:
            task_suites: List of task suites, that will be created.
            parameters: Parameters for TaskSuite creation controlling.

        Returns:
            TaskSuiteCreateBatchOperation: An operation upon completion of which you can get the created teask suites.

        Example:
            >>> task_suites = [
            >>>     toloka.task_suite.TaskSuite(
            >>>         pool_id=pool.id,
            >>>         overlap=1,
            >>>         tasks=[
            >>>             toloka.task.Task(input_values={
            >>>                 'input1': some_input_value,
            >>>                 'input2': some_input_value
            >>>             })
            >>>         ]
            >>>     )
            >>> ]
            >>> task_suites_op = toloka_client.create_task_suites_async(task_suites)
            >>> toloka_client.wait_operation(task_suites_op)
            ...
        """
        ...

    @overload
    def create_task_suites_async(
        self,
        task_suites: List[TaskSuite],
        *,
        operation_id: Optional[UUID] = None,
        skip_invalid_items: Optional[bool] = None,
        allow_defaults: Optional[bool] = None,
        open_pool: Optional[bool] = None,
        async_mode: Optional[bool] = True
    ) -> TaskSuiteCreateBatchOperation:
        """Creates many task suites in pools, asynchronous version

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Recomended maximum of 10,000 task suites per request.

        Args:
            task_suites: List of task suites, that will be created.
            parameters: Parameters for TaskSuite creation controlling.

        Returns:
            TaskSuiteCreateBatchOperation: An operation upon completion of which you can get the created teask suites.

        Example:
            >>> task_suites = [
            >>>     toloka.task_suite.TaskSuite(
            >>>         pool_id=pool.id,
            >>>         overlap=1,
            >>>         tasks=[
            >>>             toloka.task.Task(input_values={
            >>>                 'input1': some_input_value,
            >>>                 'input2': some_input_value
            >>>             })
            >>>         ]
            >>>     )
            >>> ]
            >>> task_suites_op = toloka_client.create_task_suites_async(task_suites)
            >>> toloka_client.wait_operation(task_suites_op)
            ...
        """
        ...

    @overload
    def create_tasks(
        self,
        tasks: List[Task],
        parameters: Optional[CreateTasksParameters] = None
    ) -> TaskBatchCreateResult:
        """Creates many tasks in pools

        By default uses asynchronous operation inside. It's better not to set "async_mode=False", if you not understand
        clearly why you need it.
        Tasks can be from different pools. You can insert both regular tasks and golden-tasks.
        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        Recomended maximum of 10,000 task per request if async_mode is True.

        Args:
            tasks: List of tasks, that will be created.
            parameters: Parameters for Tasks creation controlling. Defaults to None, in which case the asynchronous
                operations is used.

        Returns:
            batch_create_results.TaskBatchCreateResult: Result of tasks creating. Contains created tasks in `items` and
                problems in "validation_errors".

        Raises:
            ValidationApiError: If no tasks were created, or skip_invalid_items==False and there is a problem when
                checking any task.

        Example:
            How to create regular tasks from tsv.

            >>> dataset = pandas.read_csv('dataset.tsv', sep='  ')
            >>> tasks = [
            >>>     toloka.task.Task(input_values={'image': url}, pool_id=existing_pool_id)
            >>>     for url in dataset['image'].values[:50]
            >>> ]
            >>> created_result = toloka_client.create_tasks(tasks, allow_defaults=True)
            >>> print(len(created_result.items))
            ...

            How to create golden-tasks.

            >>> dataset = pd.read_csv('dateset.tsv', sep=';')
            >>> golden_tasks = []
            >>> for _, row in dataset.iterrows():
            >>>     golden_tasks.append(
            >>>             toloka.task.Task(
            >>>                 input_values={'image': row['image']},
            >>>                 known_solutions = [toloka.task.BaseTask.KnownSolution(output_values={'animal': row['label']})],
            >>>                 pool_id = existing_pool_id,
            >>>             )
            >>>         )
            >>> created_result = toloka_client.create_tasks(golden_tasks, allow_defaults=True)
            >>> print(len(created_result.items))
            ...
        """
        ...

    @overload
    def create_tasks(
        self,
        tasks: List[Task],
        *,
        allow_defaults: Optional[bool] = None,
        open_pool: Optional[bool] = None,
        skip_invalid_items: Optional[bool] = None,
        operation_id: Optional[UUID] = None,
        async_mode: Optional[bool] = True
    ) -> TaskBatchCreateResult:
        """Creates many tasks in pools

        By default uses asynchronous operation inside. It's better not to set "async_mode=False", if you not understand
        clearly why you need it.
        Tasks can be from different pools. You can insert both regular tasks and golden-tasks.
        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        Recomended maximum of 10,000 task per request if async_mode is True.

        Args:
            tasks: List of tasks, that will be created.
            parameters: Parameters for Tasks creation controlling. Defaults to None, in which case the asynchronous
                operations is used.

        Returns:
            batch_create_results.TaskBatchCreateResult: Result of tasks creating. Contains created tasks in `items` and
                problems in "validation_errors".

        Raises:
            ValidationApiError: If no tasks were created, or skip_invalid_items==False and there is a problem when
                checking any task.

        Example:
            How to create regular tasks from tsv.

            >>> dataset = pandas.read_csv('dataset.tsv', sep='  ')
            >>> tasks = [
            >>>     toloka.task.Task(input_values={'image': url}, pool_id=existing_pool_id)
            >>>     for url in dataset['image'].values[:50]
            >>> ]
            >>> created_result = toloka_client.create_tasks(tasks, allow_defaults=True)
            >>> print(len(created_result.items))
            ...

            How to create golden-tasks.

            >>> dataset = pd.read_csv('dateset.tsv', sep=';')
            >>> golden_tasks = []
            >>> for _, row in dataset.iterrows():
            >>>     golden_tasks.append(
            >>>             toloka.task.Task(
            >>>                 input_values={'image': row['image']},
            >>>                 known_solutions = [toloka.task.BaseTask.KnownSolution(output_values={'animal': row['label']})],
            >>>                 pool_id = existing_pool_id,
            >>>             )
            >>>         )
            >>> created_result = toloka_client.create_tasks(golden_tasks, allow_defaults=True)
            >>> print(len(created_result.items))
            ...
        """
        ...

    @overload
    def create_tasks_async(
        self,
        tasks: List[Task],
        parameters: Optional[CreateTasksParameters] = None
    ) -> TasksCreateOperation:
        """Creates many tasks in pools, asynchronous version

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        Recomended maximum of 10,000 task per request if async_mode is True.

        Args:
            tasks: List of tasks, that will be created.
            parameters: Parameters for Tasks creation controlling. Defaults to None.

        Returns:
            TasksCreateOperation: An operation upon completion of which you can get the created tasks.

        Example:
            >>> training_tasks = [
            >>>     toloka.task.Task(
            >>>                 input_values={'image': 'link1'},
            >>>                 pool_id='1'),
            >>>     toloka.task.Task(
            >>>             input_values={'image': 'link2'},
            >>>             pool_id='1')
            >>> ]
            >>> tasks_op = toloka_client.create_tasks_async(training_tasks)
            >>> toloka_client.wait_operation(tasks_op)
            ...
        """
        ...

    @overload
    def create_tasks_async(
        self,
        tasks: List[Task],
        *,
        allow_defaults: Optional[bool] = None,
        open_pool: Optional[bool] = None,
        skip_invalid_items: Optional[bool] = None,
        operation_id: Optional[UUID] = None,
        async_mode: Optional[bool] = True
    ) -> TasksCreateOperation:
        """Creates many tasks in pools, asynchronous version

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        Recomended maximum of 10,000 task per request if async_mode is True.

        Args:
            tasks: List of tasks, that will be created.
            parameters: Parameters for Tasks creation controlling. Defaults to None.

        Returns:
            TasksCreateOperation: An operation upon completion of which you can get the created tasks.

        Example:
            >>> training_tasks = [
            >>>     toloka.task.Task(
            >>>                 input_values={'image': 'link1'},
            >>>                 pool_id='1'),
            >>>     toloka.task.Task(
            >>>             input_values={'image': 'link2'},
            >>>             pool_id='1')
            >>> ]
            >>> tasks_op = toloka_client.create_tasks_async(training_tasks)
            >>> toloka_client.wait_operation(tasks_op)
            ...
        """
        ...

    def create_training(self, training: Training) -> Training:
        """Creates a new training

        Args:
            training: New Training with setted parameters.

        Returns:
            Training: Created training. With read-only fields.

        Example:
            How to create a new training in a project.

            >>> new_training = toloka.training.Training(
            >>>     project_id=existing_project_id,
            >>>     private_name='Some training in my project',
            >>>     may_contain_adult_content=True,
            >>>     assignment_max_duration_seconds=10000,
            >>>     mix_tasks_in_creation_order=True,
            >>>     shuffle_tasks_in_task_suite=True,
            >>>     training_tasks_in_task_suite_count=3,
            >>>     task_suites_required_to_pass=1,
            >>>     retry_training_after_days=7,
            >>>     inherited_instructions=True,
            >>>     public_instructions='',
            >>> )
            >>> new_training = toloka_client.create_training(new_training)
            >>> print(new_training.id)
            ...
        """
        ...

    @overload
    def create_user_bonus(
        self,
        user_bonus: UserBonus,
        parameters: Optional[UserBonusCreateRequestParameters] = None
    ) -> UserBonus:
        """Issues payments directly to the performer

        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonus: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonus: Created bonus.

        Example:
            Create bonus for specific assignment.

            >>> import decimal
            >>> new_bonus = toloka_client.create_user_bonus(
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title='Perfect job!',
            >>>         public_message='You are the best performer!',
            >>>         assignment_id='012345'
            >>>     )
            >>> )
            ...
        """
        ...

    @overload
    def create_user_bonus(
        self,
        user_bonus: UserBonus,
        *,
        operation_id: Optional[str] = None,
        skip_invalid_items: Optional[bool] = None
    ) -> UserBonus:
        """Issues payments directly to the performer

        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonus: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonus: Created bonus.

        Example:
            Create bonus for specific assignment.

            >>> import decimal
            >>> new_bonus = toloka_client.create_user_bonus(
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title='Perfect job!',
            >>>         public_message='You are the best performer!',
            >>>         assignment_id='012345'
            >>>     )
            >>> )
            ...
        """
        ...

    @overload
    def create_user_bonuses(
        self,
        user_bonuses: List[UserBonus],
        parameters: Optional[UserBonusCreateRequestParameters] = None
    ) -> UserBonusBatchCreateResult:
        """Creates many user bonuses

        Right now it's safer to use asynchronous version: "create_user_bonuses_async"
        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonuses: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonusBatchCreateResult: Result of user bonuses creating. Contains created user bonuses in `items` and
                problems in "validation_errors".

        Example:
            >>> import decimal
            >>> new_bonuses=[
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title='Perfect job!',
            >>>         public_message='You are the best performer!',
            >>>         assignment_id='1'),
            >>>     UserBonus(
            >>>         user_id='2',
            >>>         amount=decimal.Decimal('1.0'),
            >>>         public_title='Excellent work!',
            >>>         public_message='You completed all the tasks!',
            >>>         assignment_id='2')
            >>> ]
            >>> toloka_client.create_user_bonuses(new_bonuses)
            ...
        """
        ...

    @overload
    def create_user_bonuses(
        self,
        user_bonuses: List[UserBonus],
        *,
        operation_id: Optional[str] = None,
        skip_invalid_items: Optional[bool] = None
    ) -> UserBonusBatchCreateResult:
        """Creates many user bonuses

        Right now it's safer to use asynchronous version: "create_user_bonuses_async"
        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonuses: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonusBatchCreateResult: Result of user bonuses creating. Contains created user bonuses in `items` and
                problems in "validation_errors".

        Example:
            >>> import decimal
            >>> new_bonuses=[
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title='Perfect job!',
            >>>         public_message='You are the best performer!',
            >>>         assignment_id='1'),
            >>>     UserBonus(
            >>>         user_id='2',
            >>>         amount=decimal.Decimal('1.0'),
            >>>         public_title='Excellent work!',
            >>>         public_message='You completed all the tasks!',
            >>>         assignment_id='2')
            >>> ]
            >>> toloka_client.create_user_bonuses(new_bonuses)
            ...
        """
        ...

    @overload
    def create_user_bonuses_async(
        self,
        user_bonuses: List[UserBonus],
        parameters: Optional[UserBonusCreateRequestParameters] = None
    ) -> UserBonusCreateBatchOperation:
        """Issues payments directly to the performers, asynchronously creates many user bonuses

        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonuses: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonusCreateBatchOperation: An operation upon completion of which the bonuses can be considered created.

        Example:
            >>> import decimal
            >>> new_bonuses=[
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title='Perfect job!',
            >>>         public_message='You are the best performer!',
            >>>         assignment_id='1'),
            >>>     UserBonus(
            >>>         user_id='2',
            >>>         amount=decimal.Decimal('1.0'),
            >>>         public_title='Excellent work!',
            >>>         public_message='You completed all the tasks!',
            >>>         assignment_id='2')
            >>> ]
            >>> create_bonuses = toloka_client.create_user_bonuses_async(new_bonuses)
            >>> toloka_client.wait_operation(create_bonuses)
            ...
        """
        ...

    @overload
    def create_user_bonuses_async(
        self,
        user_bonuses: List[UserBonus],
        *,
        operation_id: Optional[str] = None,
        skip_invalid_items: Optional[bool] = None
    ) -> UserBonusCreateBatchOperation:
        """Issues payments directly to the performers, asynchronously creates many user bonuses

        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonuses: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonusCreateBatchOperation: An operation upon completion of which the bonuses can be considered created.

        Example:
            >>> import decimal
            >>> new_bonuses=[
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title='Perfect job!',
            >>>         public_message='You are the best performer!',
            >>>         assignment_id='1'),
            >>>     UserBonus(
            >>>         user_id='2',
            >>>         amount=decimal.Decimal('1.0'),
            >>>         public_title='Excellent work!',
            >>>         public_message='You completed all the tasks!',
            >>>         assignment_id='2')
            >>> ]
            >>> create_bonuses = toloka_client.create_user_bonuses_async(new_bonuses)
            >>> toloka_client.wait_operation(create_bonuses)
            ...
        """
        ...

    def delete_user_restriction(self, user_restriction_id: str) -> None:
        """Unlocks existing restriction

        Args:
            user_restriction_id: Restriction that should be removed.

        Example:
            >>> toloka_client.delete_user_restriction(user_restriction_id='1')
            ...
        """
        ...

    def delete_user_skill(self, user_skill_id: str) -> None:
        """Drop specific UserSkill

        UserSkill describe the skill value for a specific performer.

        Args:
            user_skill_id: ID of the fact that the performer has a skill to delete.

        Example:
            >>> toloka_client.delete_user_skill(user_skill_id='1')
            ...
        """
        ...

    def delete_webhook_subscription(self, webhook_subscription_id: str) -> None:
        """Drop specific webhook-subscription

        Args:
            webhook_subscription_id: ID of the webhook-subscription to delete.
        """
        ...

    def download_attachment(
        self,
        attachment_id: str,
        out: BinaryIO
    ) -> None:
        """Downloads specific attachment

        Args:
            attachment_id: ID of attachment.
            out: File object where to put downloaded file.

        Example:
            How to download an attachment.

            >>> with open('my_new_file.txt', 'wb') as out_f:
            >>>     toloka_client.download_attachment(attachment_id='1', out=out_f)
            ...
        """
        ...

    @overload
    def find_aggregated_solutions(
        self,
        operation_id: str,
        request: AggregatedSolutionSearchRequest,
        sort: Union[List[str], AggregatedSolutionSortItems, None] = None,
        limit: Optional[int] = None
    ) -> AggregatedSolutionSearchResult:
        """Gets aggregated responses after the AggregatedSolutionOperation completes.
        It is better to use the "get_aggregated_solutions" method, that allows to iterate through all results.

        **Note**: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
        methods and can perform on your computers: https://github.com/Toloka/crowd-kit

        Args:
            operation_id: From what aggregation operation you want to get results.
            request: How to filter search results.
            sort: How to sort results. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AggregatedSolutionSearchResult: The first `limit` solutions in `items`. And a mark that there is more.

        Example:
            How to get all aggregated solutions from pool.

            >>> # run toloka_client.aggregate_solutions_by_pool and wait operation for closing.
            >>> current_result = toloka_client.find_aggregated_solutions(aggregation_operation.id)
            >>> aggregation_results = current_result.items
            >>> # If we have more results, let's get them
            >>> while current_result.has_more:
            >>>     current_result = toloka_client.find_aggregated_solutions(
            >>>         aggregation_operation.id,
            >>>         task_id_gt=current_result.items[len(current_result.items) - 1].task_id,
            >>>     )
            >>>     aggregation_results = aggregation_results + current_result.items
            >>> print(len(aggregation_results))
            ...
        """
        ...

    @overload
    def find_aggregated_solutions(
        self,
        operation_id: str,
        task_id_lt: Optional[str] = None,
        task_id_lte: Optional[str] = None,
        task_id_gt: Optional[str] = None,
        task_id_gte: Optional[str] = None,
        sort: Union[List[str], AggregatedSolutionSortItems, None] = None,
        limit: Optional[int] = None
    ) -> AggregatedSolutionSearchResult:
        """Gets aggregated responses after the AggregatedSolutionOperation completes.
        It is better to use the "get_aggregated_solutions" method, that allows to iterate through all results.

        **Note**: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
        methods and can perform on your computers: https://github.com/Toloka/crowd-kit

        Args:
            operation_id: From what aggregation operation you want to get results.
            request: How to filter search results.
            sort: How to sort results. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AggregatedSolutionSearchResult: The first `limit` solutions in `items`. And a mark that there is more.

        Example:
            How to get all aggregated solutions from pool.

            >>> # run toloka_client.aggregate_solutions_by_pool and wait operation for closing.
            >>> current_result = toloka_client.find_aggregated_solutions(aggregation_operation.id)
            >>> aggregation_results = current_result.items
            >>> # If we have more results, let's get them
            >>> while current_result.has_more:
            >>>     current_result = toloka_client.find_aggregated_solutions(
            >>>         aggregation_operation.id,
            >>>         task_id_gt=current_result.items[len(current_result.items) - 1].task_id,
            >>>     )
            >>>     aggregation_results = aggregation_results + current_result.items
            >>> print(len(aggregation_results))
            ...
        """
        ...

    @overload
    def find_assignments(
        self,
        request: AssignmentSearchRequest,
        sort: Union[List[str], AssignmentSortItems, None] = None,
        limit: Optional[int] = None
    ) -> AssignmentSearchResult:
        """Finds all assignments that match certain rules

        As a result, it returns an object that contains the first part of the found assignments and whether there
        are any more results.
        It is better to use the "get_assignments" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search assignments.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of assignments returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AssignmentSearchResult: The first `limit` assignments in `items`. And a mark that there is more.

        Example:
            Search for `SKIPPED` or `EXPIRED` assignments in the specified pool.

            >>> toloka_client.find_assignments(pool_id='1', status = ['SKIPPED', 'EXPIRED'])
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_assignments(
        self,
        status: Union[str, Assignment.Status, List[Union[str, Assignment.Status]]] = None,
        task_id: Optional[str] = None,
        task_suite_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        user_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        submitted_lt: Optional[datetime] = None,
        submitted_lte: Optional[datetime] = None,
        submitted_gt: Optional[datetime] = None,
        submitted_gte: Optional[datetime] = None,
        accepted_lt: Optional[datetime] = None,
        accepted_lte: Optional[datetime] = None,
        accepted_gt: Optional[datetime] = None,
        accepted_gte: Optional[datetime] = None,
        rejected_lt: Optional[datetime] = None,
        rejected_lte: Optional[datetime] = None,
        rejected_gt: Optional[datetime] = None,
        rejected_gte: Optional[datetime] = None,
        skipped_lt: Optional[datetime] = None,
        skipped_lte: Optional[datetime] = None,
        skipped_gt: Optional[datetime] = None,
        skipped_gte: Optional[datetime] = None,
        expired_lt: Optional[datetime] = None,
        expired_lte: Optional[datetime] = None,
        expired_gt: Optional[datetime] = None,
        expired_gte: Optional[datetime] = None,
        sort: Union[List[str], AssignmentSortItems, None] = None,
        limit: Optional[int] = None
    ) -> AssignmentSearchResult:
        """Finds all assignments that match certain rules

        As a result, it returns an object that contains the first part of the found assignments and whether there
        are any more results.
        It is better to use the "get_assignments" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search assignments.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of assignments returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AssignmentSearchResult: The first `limit` assignments in `items`. And a mark that there is more.

        Example:
            Search for `SKIPPED` or `EXPIRED` assignments in the specified pool.

            >>> toloka_client.find_assignments(pool_id='1', status = ['SKIPPED', 'EXPIRED'])
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_attachments(
        self,
        request: AttachmentSearchRequest,
        sort: Union[List[str], AttachmentSortItems, None] = None,
        limit: Optional[int] = None
    ) -> AttachmentSearchResult:
        """Finds all attachments that match certain rules

        As a result, it returns an object that contains the first part of the found attachments and whether there
        are any more results.
        It is better to use the "get_attachments" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search attachments.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AttachmentSearchResult: The first `limit` assignments in `items`. And a mark that there is more.

        Example:
            Let's find attachments in the pool and sort them by id and date of creation.

            >>> toloka_client.find_attachments(pool_id='1', sort=['-created', '-id'], limit=10)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_attachments(
        self,
        name: Optional[str] = None,
        type: Optional[Attachment.Type] = None,
        user_id: Optional[str] = None,
        assignment_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        owner_id: Optional[str] = None,
        owner_company_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        sort: Union[List[str], AttachmentSortItems, None] = None,
        limit: Optional[int] = None
    ) -> AttachmentSearchResult:
        """Finds all attachments that match certain rules

        As a result, it returns an object that contains the first part of the found attachments and whether there
        are any more results.
        It is better to use the "get_attachments" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search attachments.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AttachmentSearchResult: The first `limit` assignments in `items`. And a mark that there is more.

        Example:
            Let's find attachments in the pool and sort them by id and date of creation.

            >>> toloka_client.find_attachments(pool_id='1', sort=['-created', '-id'], limit=10)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_message_threads(
        self,
        request: MessageThreadSearchRequest,
        sort: Union[List[str], MessageThreadSortItems, None] = None,
        limit: Optional[int] = None
    ) -> MessageThreadSearchResult:
        """Finds all message threads that match certain rules

        As a result, it returns an object that contains the first part of the found threads and whether there
        are any more results.
        It is better to use the "get_message_threads" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request:  How to search threads.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.MessageThreadSearchResult: The first `limit` message threads in `items`.
                And a mark that there is more.

        Example:
            Find all message threads in the Inbox folder.

            >>> toloka_client.find_message_threads(folder='INBOX')
            ...
        """
        ...

    @overload
    def find_message_threads(
        self,
        folder: Union[str, Folder, List[Union[str, Folder]]] = None,
        folder_ne: Union[str, Folder, List[Union[str, Folder]]] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        sort: Union[List[str], MessageThreadSortItems, None] = None,
        limit: Optional[int] = None
    ) -> MessageThreadSearchResult:
        """Finds all message threads that match certain rules

        As a result, it returns an object that contains the first part of the found threads and whether there
        are any more results.
        It is better to use the "get_message_threads" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request:  How to search threads.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.MessageThreadSearchResult: The first `limit` message threads in `items`.
                And a mark that there is more.

        Example:
            Find all message threads in the Inbox folder.

            >>> toloka_client.find_message_threads(folder='INBOX')
            ...
        """
        ...

    @overload
    def find_pools(
        self,
        request: PoolSearchRequest,
        sort: Union[List[str], PoolSortItems, None] = None,
        limit: Optional[int] = None
    ) -> PoolSearchResult:
        """Finds all pools that match certain rules

        As a result, it returns an object that contains the first part of the found pools and whether there
        are any more results.
        It is better to use the "get_pools" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search pools.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 20 results.

        Returns:
            search_results.PoolSearchResult: The first `limit` pools in `items`.
                And a mark that there is more.

        Examples:
            Find all pools in all projects.

            >>> toloka_client.find_pools()
            ...

            Find all open pools in all projects.

            >>> toloka_client.find_pools(status='OPEN')
            ...

            Find open pools in a specific project.

            >>> toloka_client.find_pools(status='OPEN', project_id='1')
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_pools(
        self,
        status: Optional[Pool.Status] = None,
        project_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        last_started_lt: Optional[datetime] = None,
        last_started_lte: Optional[datetime] = None,
        last_started_gt: Optional[datetime] = None,
        last_started_gte: Optional[datetime] = None,
        sort: Union[List[str], PoolSortItems, None] = None,
        limit: Optional[int] = None
    ) -> PoolSearchResult:
        """Finds all pools that match certain rules

        As a result, it returns an object that contains the first part of the found pools and whether there
        are any more results.
        It is better to use the "get_pools" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search pools.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 20 results.

        Returns:
            search_results.PoolSearchResult: The first `limit` pools in `items`.
                And a mark that there is more.

        Examples:
            Find all pools in all projects.

            >>> toloka_client.find_pools()
            ...

            Find all open pools in all projects.

            >>> toloka_client.find_pools(status='OPEN')
            ...

            Find open pools in a specific project.

            >>> toloka_client.find_pools(status='OPEN', project_id='1')
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_projects(
        self,
        request: ProjectSearchRequest,
        sort: Union[List[str], ProjectSortItems, None] = None,
        limit: Optional[int] = None
    ) -> ProjectSearchResult:
        """Finds all projects that match certain rules

        As a result, it returns an object that contains the first part of the found projects and whether there
        are any more results.
        It is better to use the "get_projects" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search projects.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 20 results.

        Returns:
            search_results.ProjectSearchResult: The first `limit` projects in `items`.
                And a mark that there is more.

        Example:
            Find projects that were created before a specific date.

            >>> toloka_client.find_projects(created_lt='2021-06-01T00:00:00')
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_projects(
        self,
        status: Optional[Project.ProjectStatus] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        sort: Union[List[str], ProjectSortItems, None] = None,
        limit: Optional[int] = None
    ) -> ProjectSearchResult:
        """Finds all projects that match certain rules

        As a result, it returns an object that contains the first part of the found projects and whether there
        are any more results.
        It is better to use the "get_projects" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search projects.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 20 results.

        Returns:
            search_results.ProjectSearchResult: The first `limit` projects in `items`.
                And a mark that there is more.

        Example:
            Find projects that were created before a specific date.

            >>> toloka_client.find_projects(created_lt='2021-06-01T00:00:00')
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_skills(
        self,
        request: SkillSearchRequest,
        sort: Union[List[str], SkillSortItems, None] = None,
        limit: Optional[int] = None
    ) -> SkillSearchResult:
        """Finds all skills that match certain rules

        As a result, it returns an object that contains the first part of the found skills and whether there
        are any more results.
        It is better to use the "get_skills" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search skills.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            SkillSearchResult: The first `limit` skills in `items`.
                And a mark that there is more.

        Example:
            Find ten most recently created skills.

            >>> toloka_client.find_skills(sort=['-created', '-id'], limit=10)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_skills(
        self,
        name: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        sort: Union[List[str], SkillSortItems, None] = None,
        limit: Optional[int] = None
    ) -> SkillSearchResult:
        """Finds all skills that match certain rules

        As a result, it returns an object that contains the first part of the found skills and whether there
        are any more results.
        It is better to use the "get_skills" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search skills.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            SkillSearchResult: The first `limit` skills in `items`.
                And a mark that there is more.

        Example:
            Find ten most recently created skills.

            >>> toloka_client.find_skills(sort=['-created', '-id'], limit=10)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_task_suites(
        self,
        request: TaskSuiteSearchRequest,
        sort: Union[List[str], TaskSuiteSortItems, None] = None,
        limit: Optional[int] = None
    ) -> TaskSuiteSearchResult:
        """Finds all task suites that match certain rules

        As a result, it returns an object that contains the first part of the found task suites and whether there
        are any more results.
        It is better to use the "get_task_suites" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search task suites.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100 000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            TaskSuiteSearchResult: The first `limit` task suites in `items`. And a mark that there is more.

        Example:
            Find three most recently created task suites in a specified pool.

            >>> toloka_client.find_task_suites(pool_id='1', sort=['-created', '-id'], limit=3)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_task_suites(
        self,
        task_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        overlap: Optional[int] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        overlap_lt: Optional[int] = None,
        overlap_lte: Optional[int] = None,
        overlap_gt: Optional[int] = None,
        overlap_gte: Optional[int] = None,
        sort: Union[List[str], TaskSuiteSortItems, None] = None,
        limit: Optional[int] = None
    ) -> TaskSuiteSearchResult:
        """Finds all task suites that match certain rules

        As a result, it returns an object that contains the first part of the found task suites and whether there
        are any more results.
        It is better to use the "get_task_suites" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search task suites.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100 000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            TaskSuiteSearchResult: The first `limit` task suites in `items`. And a mark that there is more.

        Example:
            Find three most recently created task suites in a specified pool.

            >>> toloka_client.find_task_suites(pool_id='1', sort=['-created', '-id'], limit=3)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_tasks(
        self,
        request: TaskSearchRequest,
        sort: Union[List[str], TaskSortItems, None] = None,
        limit: Optional[int] = None
    ) -> TaskSearchResult:
        """Finds all tasks that match certain rules

        As a result, it returns an object that contains the first part of the found tasks and whether there
        are any more results.
        It is better to use the "get_tasks" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search tasks.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100 000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            TaskSearchResult: The first `limit` tasks in `items`. And a mark that there is more.

        Example:
            Find three most recently created tasks in a specified pool.

            >>> toloka_client.find_tasks(pool_id='1', sort=['-created', '-id'], limit=3)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_tasks(
        self,
        pool_id: Optional[str] = None,
        overlap: Optional[int] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        overlap_lt: Optional[int] = None,
        overlap_lte: Optional[int] = None,
        overlap_gt: Optional[int] = None,
        overlap_gte: Optional[int] = None,
        sort: Union[List[str], TaskSortItems, None] = None,
        limit: Optional[int] = None
    ) -> TaskSearchResult:
        """Finds all tasks that match certain rules

        As a result, it returns an object that contains the first part of the found tasks and whether there
        are any more results.
        It is better to use the "get_tasks" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search tasks.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100 000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            TaskSearchResult: The first `limit` tasks in `items`. And a mark that there is more.

        Example:
            Find three most recently created tasks in a specified pool.

            >>> toloka_client.find_tasks(pool_id='1', sort=['-created', '-id'], limit=3)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_trainings(
        self,
        request: TrainingSearchRequest,
        sort: Union[List[str], TrainingSortItems, None] = None,
        limit: Optional[int] = None
    ) -> TrainingSearchResult:
        """Finds all trainings that match certain rules

        As a result, it returns an object that contains the first part of the found trainings and whether there
        are any more results.
        It is better to use the "get_trainings" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search trainings.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            search_results.TrainingSearchResult: The first `limit` trainings in `items`.
                And a mark that there is more.

        Examples:
            Find all trainings in all projects.

            >>> toloka_client.find_trainings()
            ...

            Find all open trainings in all projects.

            >>> toloka_client.find_trainings(status='OPEN')
            ...

            Find all open trainings in a specific project.

            >>> toloka_client.find_trainings(status='OPEN', project_id='1')
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_trainings(
        self,
        status: Optional[Training.Status] = None,
        project_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        last_started_lt: Optional[datetime] = None,
        last_started_lte: Optional[datetime] = None,
        last_started_gt: Optional[datetime] = None,
        last_started_gte: Optional[datetime] = None,
        sort: Union[List[str], TrainingSortItems, None] = None,
        limit: Optional[int] = None
    ) -> TrainingSearchResult:
        """Finds all trainings that match certain rules

        As a result, it returns an object that contains the first part of the found trainings and whether there
        are any more results.
        It is better to use the "get_trainings" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search trainings.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            search_results.TrainingSearchResult: The first `limit` trainings in `items`.
                And a mark that there is more.

        Examples:
            Find all trainings in all projects.

            >>> toloka_client.find_trainings()
            ...

            Find all open trainings in all projects.

            >>> toloka_client.find_trainings(status='OPEN')
            ...

            Find all open trainings in a specific project.

            >>> toloka_client.find_trainings(status='OPEN', project_id='1')
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_user_bonuses(
        self,
        request: UserBonusSearchRequest,
        sort: Union[List[str], UserBonusSortItems, None] = None,
        limit: Optional[int] = None
    ) -> UserBonusSearchResult:
        """Finds all user bonuses that match certain rules

        As a result, it returns an object that contains the first part of the found user bonuses and whether there
        are any more results.
        It is better to use the "get_user_bonuses" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user bonuses.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserBonusSearchResult: The first `limit` user bonuses in `items`.
                And a mark that there is more.

        Example:
            >>> toloka_client.find_user_bonuses(user_id='1', sort=['-created', '-id'], limit=3)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_user_bonuses(
        self,
        user_id: Optional[str] = None,
        assignment_id: Optional[str] = None,
        private_comment: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        sort: Union[List[str], UserBonusSortItems, None] = None,
        limit: Optional[int] = None
    ) -> UserBonusSearchResult:
        """Finds all user bonuses that match certain rules

        As a result, it returns an object that contains the first part of the found user bonuses and whether there
        are any more results.
        It is better to use the "get_user_bonuses" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user bonuses.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserBonusSearchResult: The first `limit` user bonuses in `items`.
                And a mark that there is more.

        Example:
            >>> toloka_client.find_user_bonuses(user_id='1', sort=['-created', '-id'], limit=3)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_user_restrictions(
        self,
        request: UserRestrictionSearchRequest,
        sort: Union[List[str], UserRestrictionSortItems, None] = None,
        limit: Optional[int] = None
    ) -> UserRestrictionSearchResult:
        """Finds all user restrictions that match certain rules

        As a result, it returns an object that contains the first part of the found user restrictions and whether there
        are any more results.
        It is better to use the "get_user_restriction" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user restrictions.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserRestrictionSearchResult: The first `limit` user restrictions in `items`.
                And a mark that there is more.

        Example:
            >>> toloka_client.find_user_restrictions(sort=['-created', '-id'], limit=10)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_user_restrictions(
        self,
        scope: Optional[UserRestriction.Scope] = None,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        sort: Union[List[str], UserRestrictionSortItems, None] = None,
        limit: Optional[int] = None
    ) -> UserRestrictionSearchResult:
        """Finds all user restrictions that match certain rules

        As a result, it returns an object that contains the first part of the found user restrictions and whether there
        are any more results.
        It is better to use the "get_user_restriction" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user restrictions.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserRestrictionSearchResult: The first `limit` user restrictions in `items`.
                And a mark that there is more.

        Example:
            >>> toloka_client.find_user_restrictions(sort=['-created', '-id'], limit=10)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_user_skills(
        self,
        request: UserSkillSearchRequest,
        sort: Union[List[str], UserSkillSortItems, None] = None,
        limit: Optional[int] = None
    ) -> UserSkillSearchResult:
        """Finds all user skills that match certain rules

        UserSkill describe the skill value for a specific performer.
        As a result, it returns an object that contains the first part of the found user skills and whether there
        are any more results.
        It is better to use the "get_user_skills" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user skills.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserSkillSearchResult: The first `limit` user skills in `items`.
                And a mark that there is more.

        Example:
            >>> toloka_client.find_user_skills(limit=10)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_user_skills(
        self,
        user_id: Optional[str] = None,
        skill_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        modified_lt: Optional[datetime] = None,
        modified_lte: Optional[datetime] = None,
        modified_gt: Optional[datetime] = None,
        modified_gte: Optional[datetime] = None,
        sort: Union[List[str], UserSkillSortItems, None] = None,
        limit: Optional[int] = None
    ) -> UserSkillSearchResult:
        """Finds all user skills that match certain rules

        UserSkill describe the skill value for a specific performer.
        As a result, it returns an object that contains the first part of the found user skills and whether there
        are any more results.
        It is better to use the "get_user_skills" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user skills.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserSkillSearchResult: The first `limit` user skills in `items`.
                And a mark that there is more.

        Example:
            >>> toloka_client.find_user_skills(limit=10)
            ...

            If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
        """
        ...

    @overload
    def find_webhook_subscriptions(
        self,
        request: WebhookSubscriptionSearchRequest,
        sort: Union[List[str], WebhookSubscriptionSortItems, None] = None,
        limit: Optional[int] = None
    ) -> WebhookSubscriptionSearchResult:
        """Finds all webhook-subscriptions that match certain rules

        As a result, it returns an object that contains the first part of the found webhook-subscriptions
        and whether there are any more results.
        It is better to use the "get_webhook_subscriptions" method, they allow to iterate through all results
        and not just the first output.

        Args:
            request: How to search webhook-subscriptions.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100 000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            WebhookSubscriptionSearchResult: The first `limit` webhook-subscriptions in `items`.
                And a mark that there is more.
        """
        ...

    @overload
    def find_webhook_subscriptions(
        self,
        event_type: Optional[WebhookSubscription.EventType] = None,
        pool_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        sort: Union[List[str], WebhookSubscriptionSortItems, None] = None,
        limit: Optional[int] = None
    ) -> WebhookSubscriptionSearchResult:
        """Finds all webhook-subscriptions that match certain rules

        As a result, it returns an object that contains the first part of the found webhook-subscriptions
        and whether there are any more results.
        It is better to use the "get_webhook_subscriptions" method, they allow to iterate through all results
        and not just the first output.

        Args:
            request: How to search webhook-subscriptions.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100 000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            WebhookSubscriptionSearchResult: The first `limit` webhook-subscriptions in `items`.
                And a mark that there is more.
        """
        ...

    @overload
    def get_aggregated_solutions(
        self,
        operation_id: str,
        request: AggregatedSolutionSearchRequest
    ) -> Generator[AggregatedSolution, None, None]:
        """Finds all aggregated responses after the AggregatedSolutionOperation completes

        **Note**: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
        methods and can perform on your computers: https://github.com/Toloka/crowd-kit

        Args:
            operation_id: From what aggregation operation you want to get results.
            request: How to filter search results.

        Yields:
            AggregatedSolution: The next object corresponding to the request parameters.

        Example:
            How to get all aggregated solutions from pool.

            >>> # run toloka_client.aggregate_solutions_by_pool and wait operation for closing.
            >>> aggregation_results = list(toloka_client.get_aggregated_solutions(aggregation_operation.id))
            ...
        """
        ...

    @overload
    def get_aggregated_solutions(
        self,
        operation_id: str,
        task_id_lt: Optional[str] = None,
        task_id_lte: Optional[str] = None,
        task_id_gt: Optional[str] = None,
        task_id_gte: Optional[str] = None
    ) -> Generator[AggregatedSolution, None, None]:
        """Finds all aggregated responses after the AggregatedSolutionOperation completes

        **Note**: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
        methods and can perform on your computers: https://github.com/Toloka/crowd-kit

        Args:
            operation_id: From what aggregation operation you want to get results.
            request: How to filter search results.

        Yields:
            AggregatedSolution: The next object corresponding to the request parameters.

        Example:
            How to get all aggregated solutions from pool.

            >>> # run toloka_client.aggregate_solutions_by_pool and wait operation for closing.
            >>> aggregation_results = list(toloka_client.get_aggregated_solutions(aggregation_operation.id))
            ...
        """
        ...

    def get_analytics(self, stats: List[AnalyticsRequest]) -> Operation:
        """Sends analytics queries, for example, to estimate the percentage of completed tasks in the pool

        Only pool analytics queries are available.
        The values of different analytical metrics will be returned in the "details" field of the operation when it is
        completed. See the example.
        You can request up to 10 metrics at a time.

        Args:
            stats: Analytics queries list.

        Returns:
            operations.Operation: An operation that you can wait for to get the required statistics.

        Example:
            How to get task completion percentage for one pool.

            >>> from toloka.client.analytics_request import CompletionPercentagePoolAnalytics
            >>> operation = toloka_client.get_analytics([CompletionPercentagePoolAnalytics(subject_id=pool_id)])
            >>> operation = toloka_client.wait_operation(operation)
            >>> print(op.details['value'][0]['result']['value'])
            ...
        """
        ...

    def get_assignment(self, assignment_id: str) -> Assignment:
        """Reads one specific assignment

        Args:
            assignment_id: ID of assignment.

        Returns:
            Assignment: The solution read as a result.

        Example:
            >>> toloka_client.get_assignment(assignment_id='1')
            ...
        """
        ...

    @overload
    def get_assignments(self, request: AssignmentSearchRequest) -> Generator[Assignment, None, None]:
        """Finds all assignments that match certain rules and returns them in an iterable object

        Unlike find_assignments, returns generator. Does not sort assignments.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search assignments.

        Yields:
            Assignment: The next object corresponding to the request parameters.

        Example:
            Let’s make a list of `assignment_id` of all `SUBMITTED` assignments in the specified pool.

            >>> from toloka.client import Assignment
            >>> assignments = toloka_client.get_assignments(pool_id='1', status=Assignment.SUBMITTED)
            >>> result_list = [assignment.id for assignment in assignments]
            ...
        """
        ...

    @overload
    def get_assignments(
        self,
        status: Union[str, Assignment.Status, List[Union[str, Assignment.Status]]] = None,
        task_id: Optional[str] = None,
        task_suite_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        user_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        submitted_lt: Optional[datetime] = None,
        submitted_lte: Optional[datetime] = None,
        submitted_gt: Optional[datetime] = None,
        submitted_gte: Optional[datetime] = None,
        accepted_lt: Optional[datetime] = None,
        accepted_lte: Optional[datetime] = None,
        accepted_gt: Optional[datetime] = None,
        accepted_gte: Optional[datetime] = None,
        rejected_lt: Optional[datetime] = None,
        rejected_lte: Optional[datetime] = None,
        rejected_gt: Optional[datetime] = None,
        rejected_gte: Optional[datetime] = None,
        skipped_lt: Optional[datetime] = None,
        skipped_lte: Optional[datetime] = None,
        skipped_gt: Optional[datetime] = None,
        skipped_gte: Optional[datetime] = None,
        expired_lt: Optional[datetime] = None,
        expired_lte: Optional[datetime] = None,
        expired_gt: Optional[datetime] = None,
        expired_gte: Optional[datetime] = None
    ) -> Generator[Assignment, None, None]:
        """Finds all assignments that match certain rules and returns them in an iterable object

        Unlike find_assignments, returns generator. Does not sort assignments.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search assignments.

        Yields:
            Assignment: The next object corresponding to the request parameters.

        Example:
            Let’s make a list of `assignment_id` of all `SUBMITTED` assignments in the specified pool.

            >>> from toloka.client import Assignment
            >>> assignments = toloka_client.get_assignments(pool_id='1', status=Assignment.SUBMITTED)
            >>> result_list = [assignment.id for assignment in assignments]
            ...
        """
        ...

    @overload
    def get_assignments_df(
        self,
        pool_id: str,
        parameters: GetAssignmentsTsvParameters
    ) -> DataFrame:
        """Downloads assignments as pandas.DataFrame

        Experimental method.
        Implements the same behavior as if you download results in web-interface and then read it by pandas.

        Args:
            pool_id: From which pool the results are loaded.
            parameters: Filters for the results and the set of fields that will be in the dataframe.

        Returns:
            pd.DataFrame: DataFrame with all results. Contains groups of fields with prefixes:
                * "INPUT" - Fields that were at the input in the task.
                * "OUTPUT" - Fields that were received as a result of execution.
                * "GOLDEN" - Fields with correct answers. Filled in only for golden tasks and training tasks.
                * "HINT" - Hints for completing tasks. Filled in for training tasks.
                * "ACCEPT" - Fields describing the deferred acceptance of tasks.
                * "ASSIGNMENT" - fields describing additional information about the Assignment.

        Example:
            Get all assignments from the specified pool by `pool_id` to [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).
            And apply the native pandas `rename` method to change columns' names.

            >>> answers_df = toloka_client.get_assignments_df(pool_id='1')
            >>> answers_df = answers_df.rename(columns={
            >>>     'INPUT:image': 'task',
            >>>     'OUTPUT:result': 'label',
            >>>     'ASSIGNMENT:worker_id': 'performer'
            >>> })
            ...
        """
        ...

    @overload
    def get_assignments_df(
        self,
        pool_id: str,
        *,
        status: Optional[List[GetAssignmentsTsvParameters.Status]] = ...,
        start_time_from: Optional[datetime] = None,
        start_time_to: Optional[datetime] = None,
        exclude_banned: Optional[bool] = None,
        field: Optional[List[GetAssignmentsTsvParameters.Field]] = ...
    ) -> DataFrame:
        """Downloads assignments as pandas.DataFrame

        Experimental method.
        Implements the same behavior as if you download results in web-interface and then read it by pandas.

        Args:
            pool_id: From which pool the results are loaded.
            parameters: Filters for the results and the set of fields that will be in the dataframe.

        Returns:
            pd.DataFrame: DataFrame with all results. Contains groups of fields with prefixes:
                * "INPUT" - Fields that were at the input in the task.
                * "OUTPUT" - Fields that were received as a result of execution.
                * "GOLDEN" - Fields with correct answers. Filled in only for golden tasks and training tasks.
                * "HINT" - Hints for completing tasks. Filled in for training tasks.
                * "ACCEPT" - Fields describing the deferred acceptance of tasks.
                * "ASSIGNMENT" - fields describing additional information about the Assignment.

        Example:
            Get all assignments from the specified pool by `pool_id` to [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).
            And apply the native pandas `rename` method to change columns' names.

            >>> answers_df = toloka_client.get_assignments_df(pool_id='1')
            >>> answers_df = answers_df.rename(columns={
            >>>     'INPUT:image': 'task',
            >>>     'OUTPUT:result': 'label',
            >>>     'ASSIGNMENT:worker_id': 'performer'
            >>> })
            ...
        """
        ...

    def get_attachment(self, attachment_id: str) -> Attachment:
        """Gets attachment metadata without downloading it

        To download attachments as a file use "TolokaClient.download_attachment" method.

        Args:
            attachment_id: ID of attachment.

        Returns:
            Attachment: The attachment metadata read as a result.

        Example:
            Specify an `attachment_id` to get the information about any attachment object.

            >>> toloka_client.get_attachment(attachment_id='1')
            ...
        """
        ...

    @overload
    def get_attachments(self, request: AttachmentSearchRequest) -> Generator[Attachment, None, None]:
        """Finds all attachments that match certain rules and returns their metadata in an iterable object

        Unlike find_attachments, returns generator. Does not sort attachments.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search attachments.

        Yields:
            Attachment: The next object corresponding to the request parameters.

        Example:
            Make a list of all received attachments in the specified pool.

            >>> results_list = [attachment for attachment in toloka_client.get_attachments(pool_id='1')]
            ...
        """
        ...

    @overload
    def get_attachments(
        self,
        name: Optional[str] = None,
        type: Optional[Attachment.Type] = None,
        user_id: Optional[str] = None,
        assignment_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        owner_id: Optional[str] = None,
        owner_company_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None
    ) -> Generator[Attachment, None, None]:
        """Finds all attachments that match certain rules and returns their metadata in an iterable object

        Unlike find_attachments, returns generator. Does not sort attachments.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search attachments.

        Yields:
            Attachment: The next object corresponding to the request parameters.

        Example:
            Make a list of all received attachments in the specified pool.

            >>> results_list = [attachment for attachment in toloka_client.get_attachments(pool_id='1')]
            ...
        """
        ...

    @overload
    def get_message_threads(self, request: MessageThreadSearchRequest) -> Generator[MessageThread, None, None]:
        """Finds all message threads that match certain rules and returns them in an iterable object

        Unlike find_message_threads, returns generator. Does not sort threads.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search attachments.

        Yields:
            MessageThread: The next object corresponding to the request parameters.

        Example:
            How to get all unread incoming messages.

            >>> message_threads = toloka_client.get_message_threads(folder=['INBOX', 'UNREAD'])
            ...
        """
        ...

    @overload
    def get_message_threads(
        self,
        folder: Union[str, Folder, List[Union[str, Folder]]] = None,
        folder_ne: Union[str, Folder, List[Union[str, Folder]]] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None
    ) -> Generator[MessageThread, None, None]:
        """Finds all message threads that match certain rules and returns them in an iterable object

        Unlike find_message_threads, returns generator. Does not sort threads.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search attachments.

        Yields:
            MessageThread: The next object corresponding to the request parameters.

        Example:
            How to get all unread incoming messages.

            >>> message_threads = toloka_client.get_message_threads(folder=['INBOX', 'UNREAD'])
            ...
        """
        ...

    def get_operation(self, operation_id: str) -> Operation:
        """Reads information about operation

        All asynchronous actions in Toloka works via operations. If you have some "Operation" usually you need to use
        "wait_operation" method.

        Args:
            operation_id: ID of the operation.

        Returns:
            Operation: The operation.

        Example:
            >>> op = toloka_client.get_operation(operation_id='1')
            ...
        """
        ...

    def get_operation_log(self, operation_id: str) -> List[OperationLogItem]:
        """Reads information about validation errors and which task (or task suites) were created

        You don't need to call this method if you use "create_tasks" for creating tasks ("create_task_suites" for task suites).
        By asynchronous creating multiple tasks (or task sets) you can get the operation log.
        Logs are only available for the last month.

        Args:
            operation_id: ID of the operation.

        Returns:
            List[OperationLogItem]: Logs for the operation.

        Example:
            >>> op = toloka_client.get_operation_log(operation_id='1')
            ...
        """
        ...

    def get_pool(self, pool_id: str) -> Pool:
        """Reads one specific pool

        Args:
            pool_id: ID of the pool.

        Returns:
            Pool: The pool.

        Example:
            >>> toloka_client.get_pool(pool_id='1')
            ...
        """
        ...

    @overload
    def get_pools(self, request: PoolSearchRequest) -> Generator[Pool, None, None]:
        """Finds all pools that match certain rules and returns them in an iterable object

        Unlike find_pools, returns generator. Does not sort pools.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search pools.

        Yields:
            Pool: The next object corresponding to the request parameters.

        Example:
            How to get all open pools from project.

            >>> open_pools = toloka_client.get_pools(project_id='1', status='OPEN')
            ...

            How to get all pools from project.

            >>> all_pools = toloka_client.get_pools(project_id='1')
            ...
        """
        ...

    @overload
    def get_pools(
        self,
        status: Optional[Pool.Status] = None,
        project_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        last_started_lt: Optional[datetime] = None,
        last_started_lte: Optional[datetime] = None,
        last_started_gt: Optional[datetime] = None,
        last_started_gte: Optional[datetime] = None
    ) -> Generator[Pool, None, None]:
        """Finds all pools that match certain rules and returns them in an iterable object

        Unlike find_pools, returns generator. Does not sort pools.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search pools.

        Yields:
            Pool: The next object corresponding to the request parameters.

        Example:
            How to get all open pools from project.

            >>> open_pools = toloka_client.get_pools(project_id='1', status='OPEN')
            ...

            How to get all pools from project.

            >>> all_pools = toloka_client.get_pools(project_id='1')
            ...
        """
        ...

    def get_project(self, project_id: str) -> Project:
        """Reads one specific project

        Args:
            project_id: ID of the project.

        Returns:
            Project: The project.

        Example:
            >>> toloka_client.get_project(project_id='1')
            ...
        """
        ...

    @overload
    def get_projects(self, request: ProjectSearchRequest) -> Generator[Project, None, None]:
        """Finds all projects that match certain rules and returns them in an iterable object

        Unlike find_projects, returns generator. Does not sort projects.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search projects.

        Yields:
            Project: The next object corresponding to the request parameters.

        Example:
            Get all active projects.

            >>> active_projects = toloka_client.get_projects(status='ACTIVE')
            ...

            Get all your projects.

            >>> my_projects = toloka_client.get_projects()
            ...
        """
        ...

    @overload
    def get_projects(
        self,
        status: Optional[Project.ProjectStatus] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None
    ) -> Generator[Project, None, None]:
        """Finds all projects that match certain rules and returns them in an iterable object

        Unlike find_projects, returns generator. Does not sort projects.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search projects.

        Yields:
            Project: The next object corresponding to the request parameters.

        Example:
            Get all active projects.

            >>> active_projects = toloka_client.get_projects(status='ACTIVE')
            ...

            Get all your projects.

            >>> my_projects = toloka_client.get_projects()
            ...
        """
        ...

    def get_requester(self) -> Requester:
        """Reads information about the customer and the account balance

        Returns:
            Requester: Object that contains all information about customer.

        Examples:
            Make sure that you've entered a valid OAuth token.

            >>> toloka_client.get_requester()
            ...

            You can also estimate approximate pipeline costs and check if there is enough money on your account.

            >>> requester = toloka_client.get_requester()
            >>> if requester.balance >= approx_pipeline_price:
            >>>     print('You have enough money on your account!')
            >>> else:
            >>>     print('You haven't got enough money on your account!')
            ...
        """
        ...

    def get_skill(self, skill_id: str) -> Skill:
        """Reads one specific skill

        Args:
            skill_id: ID of the skill.

        Returns:
            Skill: The skill.

        Example:
            >>> toloka_client.get_skill(skill_id='1')
            ...
        """
        ...

    @overload
    def get_skills(self, request: SkillSearchRequest) -> Generator[Skill, None, None]:
        """Finds all skills that match certain rules and returns them in an iterable object

        Unlike find_skills, returns generator. Does not sort skills.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search skills.

        Yields:
            Skill: The next object corresponding to the request parameters.

        Example:
            How to check that a skill exists.

            >>> segmentation_skill = next(toloka_client.get_skills(name='Area selection of road signs'), None)
            >>> if segmentation_skill:
            >>>     print(f'Segmentation skill already exists, with id {segmentation_skill.id}')
            >>> else:
            >>>     print('Create new segmentation skill here')
            ...
        """
        ...

    @overload
    def get_skills(
        self,
        name: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None
    ) -> Generator[Skill, None, None]:
        """Finds all skills that match certain rules and returns them in an iterable object

        Unlike find_skills, returns generator. Does not sort skills.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search skills.

        Yields:
            Skill: The next object corresponding to the request parameters.

        Example:
            How to check that a skill exists.

            >>> segmentation_skill = next(toloka_client.get_skills(name='Area selection of road signs'), None)
            >>> if segmentation_skill:
            >>>     print(f'Segmentation skill already exists, with id {segmentation_skill.id}')
            >>> else:
            >>>     print('Create new segmentation skill here')
            ...
        """
        ...

    def get_task(self, task_id: str) -> Task:
        """Reads one specific task

        Args:
            task_id: ID of the task.

        Returns:
            Task: The task.

        Example:
            >>> toloka_client.get_task(task_id='1')
            ...
        """
        ...

    def get_task_suite(self, task_suite_id: str) -> TaskSuite:
        """Reads one specific task suite

        Args:
            task_suite_id: ID of the task suite.

        Returns:
            TaskSuite: The task suite.

        Example:
            >>> toloka_client.get_task_suite(task_suite_id='1')
            ...
        """
        ...

    @overload
    def get_task_suites(self, request: TaskSuiteSearchRequest) -> Generator[TaskSuite, None, None]:
        """Finds all task suites that match certain rules and returns them in an iterable object

        Unlike find_task_suites, returns generator. Does not sort task suites.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search task suites.

        Yields:
            TaskSuite: The next object corresponding to the request parameters.

        Example:
            Get task suites from a specific pool.

            >>> results_list = [task_suite for task_suite in toloka_client.get_task_suites(pool_id='1')]
            ...
        """
        ...

    @overload
    def get_task_suites(
        self,
        task_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        overlap: Optional[int] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        overlap_lt: Optional[int] = None,
        overlap_lte: Optional[int] = None,
        overlap_gt: Optional[int] = None,
        overlap_gte: Optional[int] = None
    ) -> Generator[TaskSuite, None, None]:
        """Finds all task suites that match certain rules and returns them in an iterable object

        Unlike find_task_suites, returns generator. Does not sort task suites.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search task suites.

        Yields:
            TaskSuite: The next object corresponding to the request parameters.

        Example:
            Get task suites from a specific pool.

            >>> results_list = [task_suite for task_suite in toloka_client.get_task_suites(pool_id='1')]
            ...
        """
        ...

    @overload
    def get_tasks(self, request: TaskSearchRequest) -> Generator[Task, None, None]:
        """Finds all tasks that match certain rules and returns them in an iterable object

        Unlike find_tasks, returns generator. Does not sort tasks.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search tasks.

        Yields:
            Task: The next object corresponding to the request parameters.

        Example:
            Get tasks from a specific pool.

            >>> results_list = [task for task in toloka_client.get_tasks(pool_id='1')]
            ...
        """
        ...

    @overload
    def get_tasks(
        self,
        pool_id: Optional[str] = None,
        overlap: Optional[int] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        overlap_lt: Optional[int] = None,
        overlap_lte: Optional[int] = None,
        overlap_gt: Optional[int] = None,
        overlap_gte: Optional[int] = None
    ) -> Generator[Task, None, None]:
        """Finds all tasks that match certain rules and returns them in an iterable object

        Unlike find_tasks, returns generator. Does not sort tasks.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search tasks.

        Yields:
            Task: The next object corresponding to the request parameters.

        Example:
            Get tasks from a specific pool.

            >>> results_list = [task for task in toloka_client.get_tasks(pool_id='1')]
            ...
        """
        ...

    def get_training(self, training_id: str) -> Training:
        """Reads one specific training

        Args:
            training_id: ID of the training.

        Returns:
            Training: The training.

        Example:
            >>> toloka_client.get_training(training_id='1')
            ...
        """
        ...

    @overload
    def get_trainings(self, request: TrainingSearchRequest) -> Generator[Training, None, None]:
        """Finds all trainings that match certain rules and returns them in an iterable object

        Unlike find_trainings, returns generator. Does not sort trainings.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search trainings.

        Yields:
            Training: The next object corresponding to the request parameters.

        Example:
            How to get all trainings in project.

            >>> trainings = toloka_client.get_trainings(project_id=project_id)
            ...
        """
        ...

    @overload
    def get_trainings(
        self,
        status: Optional[Training.Status] = None,
        project_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        last_started_lt: Optional[datetime] = None,
        last_started_lte: Optional[datetime] = None,
        last_started_gt: Optional[datetime] = None,
        last_started_gte: Optional[datetime] = None
    ) -> Generator[Training, None, None]:
        """Finds all trainings that match certain rules and returns them in an iterable object

        Unlike find_trainings, returns generator. Does not sort trainings.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search trainings.

        Yields:
            Training: The next object corresponding to the request parameters.

        Example:
            How to get all trainings in project.

            >>> trainings = toloka_client.get_trainings(project_id=project_id)
            ...
        """
        ...

    def get_user_bonus(self, user_bonus_id: str) -> UserBonus:
        """Reads one specific user bonus

        Args:
            user_bonus_id: ID of the user bonus.

        Returns:
            UserBonus: The user bonus.

        Example:
            >>> toloka_client.get_user_bonus(user_bonus_id='1')
            ...
        """
        ...

    @overload
    def get_user_bonuses(self, request: UserBonusSearchRequest) -> Generator[UserBonus, None, None]:
        """Finds all user bonuses that match certain rules and returns them in an iterable object

        Unlike find_user_bonuses, returns generator. Does not sort user bonuses.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user bonus.

        Yields:
            UserBonus: The next object corresponding to the request parameters.

        Example:
            >>> bonuses = [bonus for bonus in toloka_client.get_user_bonuses(created_lt='2021-06-01T00:00:00')]
            ...
        """
        ...

    @overload
    def get_user_bonuses(
        self,
        user_id: Optional[str] = None,
        assignment_id: Optional[str] = None,
        private_comment: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None
    ) -> Generator[UserBonus, None, None]:
        """Finds all user bonuses that match certain rules and returns them in an iterable object

        Unlike find_user_bonuses, returns generator. Does not sort user bonuses.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user bonus.

        Yields:
            UserBonus: The next object corresponding to the request parameters.

        Example:
            >>> bonuses = [bonus for bonus in toloka_client.get_user_bonuses(created_lt='2021-06-01T00:00:00')]
            ...
        """
        ...

    def get_user_restriction(self, user_restriction_id: str) -> UserRestriction:
        """Reads one specific user restriction

        Args:
            user_restriction_id: ID of the user restriction.

        Returns:
            UserRestriction: The user restriction.

        Example:
            >>> toloka_client.get_user_restriction(user_restriction_id='1')
            ...
        """
        ...

    @overload
    def get_user_restrictions(self, request: UserRestrictionSearchRequest) -> Generator[UserRestriction, None, None]:
        """Finds all user restrictions that match certain rules and returns them in an iterable object

        Unlike find_user_restrictions, returns generator. Does not sort user restrictions.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user restrictions.

        Yields:
            UserRestriction: The next object corresponding to the request parameters.

        Example:
            >>> results_list = [restriction for restriction in toloka_client.get_user_restrictions(scope='ALL_PROJECTS')]
            ...
        """
        ...

    @overload
    def get_user_restrictions(
        self,
        scope: Optional[UserRestriction.Scope] = None,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        pool_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None
    ) -> Generator[UserRestriction, None, None]:
        """Finds all user restrictions that match certain rules and returns them in an iterable object

        Unlike find_user_restrictions, returns generator. Does not sort user restrictions.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user restrictions.

        Yields:
            UserRestriction: The next object corresponding to the request parameters.

        Example:
            >>> results_list = [restriction for restriction in toloka_client.get_user_restrictions(scope='ALL_PROJECTS')]
            ...
        """
        ...

    def get_user_skill(self, user_skill_id: str) -> UserSkill:
        """Gets the value of the user's skill

        UserSkill describe the skill value for a specific performer.

        Args:
            user_skill_id: ID of the user skill.

        Returns:
            UserSkill: The skill value.

        Example:
            >>> toloka_client.get_user_skill(user_skill_id='1')
            ...
        """
        ...

    @overload
    def get_user_skills(self, request: UserSkillSearchRequest) -> Generator[UserSkill, None, None]:
        """Finds all user skills that match certain rules and returns them in an iterable object

        UserSkill describe the skill value for a specific performer.
        Unlike find_user_skills, returns generator. Does not sort user skills.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user skills.

        Yields:
            UserSkill: The next object corresponding to the request parameters.

        Example:
            >>> results_list = [skill for skill in toloka_client.get_user_skills()]
            ...
        """
        ...

    @overload
    def get_user_skills(
        self,
        user_id: Optional[str] = None,
        skill_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None,
        modified_lt: Optional[datetime] = None,
        modified_lte: Optional[datetime] = None,
        modified_gt: Optional[datetime] = None,
        modified_gte: Optional[datetime] = None
    ) -> Generator[UserSkill, None, None]:
        """Finds all user skills that match certain rules and returns them in an iterable object

        UserSkill describe the skill value for a specific performer.
        Unlike find_user_skills, returns generator. Does not sort user skills.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user skills.

        Yields:
            UserSkill: The next object corresponding to the request parameters.

        Example:
            >>> results_list = [skill for skill in toloka_client.get_user_skills()]
            ...
        """
        ...

    def get_webhook_subscription(self, webhook_subscription_id: str) -> WebhookSubscription:
        """Get one specific webhook-subscription

        Args:
            webhook_subscription_id: ID of the subscription.

        Returns:
            WebhookSubscription: The subscription.
        """
        ...

    @overload
    def get_webhook_subscriptions(self, request: WebhookSubscriptionSearchRequest) -> Generator[WebhookSubscription, None, None]:
        """Finds all webhook-subscriptions that match certain rules and returns them in an iterable object

        Unlike find_webhook-subscriptions, returns generator. Does not sort webhook-subscriptions.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search webhook-subscriptions.

        Yields:
            WebhookSubscription: The next object corresponding to the request parameters.
        """
        ...

    @overload
    def get_webhook_subscriptions(
        self,
        event_type: Optional[WebhookSubscription.EventType] = None,
        pool_id: Optional[str] = None,
        id_lt: Optional[str] = None,
        id_lte: Optional[str] = None,
        id_gt: Optional[str] = None,
        id_gte: Optional[str] = None,
        created_lt: Optional[datetime] = None,
        created_lte: Optional[datetime] = None,
        created_gt: Optional[datetime] = None,
        created_gte: Optional[datetime] = None
    ) -> Generator[WebhookSubscription, None, None]:
        """Finds all webhook-subscriptions that match certain rules and returns them in an iterable object

        Unlike find_webhook-subscriptions, returns generator. Does not sort webhook-subscriptions.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search webhook-subscriptions.

        Yields:
            WebhookSubscription: The next object corresponding to the request parameters.
        """
        ...

    def open_pool(self, pool_id: str) -> Pool:
        """Starts distributing tasks from the pool

        Performers will see your tasks only after that call.

        Args:
            pool_id: ID of the pool that will be started.

        Returns:
            Pool: Pool object with new status.

        Example:
            Open the pool for performers.

            >>> toloka_client.open_pool(pool_id='1')
            ...
        """
        ...

    def open_pool_async(self, pool_id: str) -> PoolOpenOperation:
        """Starts distributing tasks from the pool, asynchronous version

        Performers will see your tasks only after that call.

        Args:
            pool_id: ID of the pool that will be started.

        Returns:
            PoolOpenOperation: An operation upon completion of which you can get the pool with new status.

        Example:
            Open the pool for performers.

            >>> open_pool = toloka_client.open_pool(pool_id='1')
            >>> toloka_client.wait_operation(open_pool)
            ...
        """
        ...

    def open_training(self, training_id: str) -> Training:
        """Starts distributing tasks from the training

        Args:
            training_id: ID of the training that will be started.

        Returns:
            Training: Training object with new status.

        Example:
            Open the training for performers.

            >>> toloka_client.open_training(training_id='1')
            ...
        """
        ...

    def open_training_async(self, training_id: str) -> TrainingOpenOperation:
        """Starts distributing tasks from the training, asynchronous version

        Args:
            training_id: ID of the training that will be started.

        Returns:
            TrainingOpenOperation: An operation upon completion of which you can get the training with new status.

        Example:
            Open the training for performers.

            >>> open_training = toloka_client.open_training_async(training_id='1')
            >>> toloka_client.wait_operation(open_training)
            ...
        """
        ...

    @overload
    def patch_assignment(
        self,
        assignment_id: str,
        patch: AssignmentPatch
    ) -> Assignment:
        """Changes status and comment on assignment

        It's better to use methods "reject_assignment" and "accept_assignment".

        Args:
            assignment_id: What assignment will be affected.
            patch: Object with new status and comment.

        Returns:
            Assignment: Object with new status.

        Example:
            >>> toloka_client.patch_assignment(assignment_id='1', public_comment='Some issues present, but work is acceptable', status='ACCEPTED')
            ...
        """
        ...

    @overload
    def patch_assignment(
        self,
        assignment_id: str,
        *,
        public_comment: Optional[str] = None,
        status: Optional[Assignment.Status] = None
    ) -> Assignment:
        """Changes status and comment on assignment

        It's better to use methods "reject_assignment" and "accept_assignment".

        Args:
            assignment_id: What assignment will be affected.
            patch: Object with new status and comment.

        Returns:
            Assignment: Object with new status.

        Example:
            >>> toloka_client.patch_assignment(assignment_id='1', public_comment='Some issues present, but work is acceptable', status='ACCEPTED')
            ...
        """
        ...

    @overload
    def patch_pool(
        self,
        pool_id: str,
        request: PoolPatchRequest
    ) -> Pool:
        """Changes the priority of the pool issue

        Args:
            pool_id: ID of the pool that will be patched.
            request: New priority of the pool.

        Returns:
            Pool: Object with updated priority.

        Example:
            Set the highest priority to a specified pool.

            >>> toloka_client.patch_pool(pool_id='1', priority=100)
            ...
        """
        ...

    @overload
    def patch_pool(
        self,
        pool_id: str,
        priority: Optional[int] = None
    ) -> Pool:
        """Changes the priority of the pool issue

        Args:
            pool_id: ID of the pool that will be patched.
            request: New priority of the pool.

        Returns:
            Pool: Object with updated priority.

        Example:
            Set the highest priority to a specified pool.

            >>> toloka_client.patch_pool(pool_id='1', priority=100)
            ...
        """
        ...

    @overload
    def patch_task(
        self,
        task_id: str,
        patch: TaskPatch
    ) -> Task:
        """Changes the task overlap

        Args:
            task_id: ID of the task that will be changed.
            patch: New overlap value.

        Returns:
            Task: Task with updated fields.
        """
        ...

    @overload
    def patch_task(
        self,
        task_id: str,
        *,
        overlap: Optional[int] = None,
        infinite_overlap: Optional[bool] = None,
        baseline_solutions: Optional[List[Task.BaselineSolution]] = None
    ) -> Task:
        """Changes the task overlap

        Args:
            task_id: ID of the task that will be changed.
            patch: New overlap value.

        Returns:
            Task: Task with updated fields.
        """
        ...

    @overload
    def patch_task_overlap_or_min(
        self,
        task_id: str,
        patch: TaskOverlapPatch
    ) -> Task:
        """Stops issuing the task

        Args:
            task_id: ID of the task.
            patch: New overlap value.

        Returns:
            Task: Task with updated fields.

        Example:
            Set an infinite overlap for a specific task in training.

            >>> toloka_client.patch_task_overlap_or_min(task_id='1', infinite_overlap=True)
            ...

            **Note**: you can't set infinite overlap in a regular pool.
        """
        ...

    @overload
    def patch_task_overlap_or_min(
        self,
        task_id: str,
        *,
        overlap: Optional[int] = None,
        infinite_overlap: Optional[bool] = None
    ) -> Task:
        """Stops issuing the task

        Args:
            task_id: ID of the task.
            patch: New overlap value.

        Returns:
            Task: Task with updated fields.

        Example:
            Set an infinite overlap for a specific task in training.

            >>> toloka_client.patch_task_overlap_or_min(task_id='1', infinite_overlap=True)
            ...

            **Note**: you can't set infinite overlap in a regular pool.
        """
        ...

    @overload
    def patch_task_suite(
        self,
        task_suite_id: str,
        patch: TaskSuitePatch
    ) -> TaskSuite:
        """Changes the task suite overlap or priority

        Args:
            task_suite_id: ID of the task suite that will be changed.
            patch: New values.

        Returns:
            TaskSuite: Task suite with updated fields.

        Example:
            Change the task suite's priority.

            >>> toloka_client.patch_task_suite(task_suite_id='1', issuing_order_override=100)
            ...
        """
        ...

    @overload
    def patch_task_suite(
        self,
        task_suite_id: str,
        *,
        infinite_overlap=None,
        overlap=None,
        issuing_order_override: Optional[float] = None,
        open_pool: Optional[bool] = None
    ) -> TaskSuite:
        """Changes the task suite overlap or priority

        Args:
            task_suite_id: ID of the task suite that will be changed.
            patch: New values.

        Returns:
            TaskSuite: Task suite with updated fields.

        Example:
            Change the task suite's priority.

            >>> toloka_client.patch_task_suite(task_suite_id='1', issuing_order_override=100)
            ...
        """
        ...

    @overload
    def patch_task_suite_overlap_or_min(
        self,
        task_suite_id: str,
        patch: TaskSuiteOverlapPatch
    ) -> TaskSuite:
        """Stops issuing the task suites

        Args:
            task_suite_id: ID of the task suite.
            patch: New overlap value.

        Returns:
            TaskSuite: Task suite with updated fields.

        Example:
            >>> toloka_client.patch_task_suite_overlap_or_min(task_suite_id='1', overlap=100)
            ...
        """
        ...

    @overload
    def patch_task_suite_overlap_or_min(
        self,
        task_suite_id: str,
        *,
        overlap: Optional[int] = None
    ) -> TaskSuite:
        """Stops issuing the task suites

        Args:
            task_suite_id: ID of the task suite.
            patch: New overlap value.

        Returns:
            TaskSuite: Task suite with updated fields.

        Example:
            >>> toloka_client.patch_task_suite_overlap_or_min(task_suite_id='1', overlap=100)
            ...
        """
        ...

    def reject_assignment(
        self,
        assignment_id: str,
        public_comment: str
    ) -> Assignment:
        """Marks one assignment as rejected

        Used then your pool created with auto_accept_solutions=False parametr.

        Args:
            assignment_id: What assignment will be rejected.
            public_comment: Message to the performer.

        Returns:
            Assignment: Object with new status.

        Example:
            Reject an assignment that was completed too fast.

            >>> toloka_client.reject_assignment(assignment_id='1', 'Assignment was completed too fast.')
            ...
        """
        ...

    def remove_message_thread_from_folders(
        self,
        message_thread_id: str,
        folders: Union[List[Folder], MessageThreadFolders]
    ) -> MessageThread:
        """Deletes a message chain from one or more folders ("unread", "important" etc.)

        Args:
            message_thread_id: ID of message chain.
            folders:  List of folders, where from to remove chain.

        Returns:
            MessageThread: Full object by ID with updated folders.

        Example:
            >>> toloka_client.remove_message_thread_from_folders(message_thread_id='1', folders=['IMPORTANT'])
            ...
        """
        ...

    def reply_message_thread(
        self,
        message_thread_id: str,
        reply: MessageThreadReply
    ) -> MessageThread:
        """Replies to a message in thread

        Args:
            message_thread_id: In which thread to reply.
            reply: Reply message.

        Returns:
            MessageThread: New created message.

        Example:
            >>> message_threads = toloka_client.get_message_threads(folder='UNREAD')
            >>> message_reply = {'EN': 'Thank you for your message! I will get back to you soon.'}
            >>> for thread in message_threads:
            >>>     toloka_client.reply_message_thread(message_thread_id=thread.id, reply=toloka.message_thread.MessageThreadReply(text=message_reply))
            ...
        """
        ...

    def set_user_restriction(self, user_restriction: UserRestriction) -> UserRestriction:
        """Closes the performer's access to one or more projects

        Args:
            user_restriction: To whom and what to prohibit.

        Returns:
            UserRestriction: Created restriction object.

        Example:
            If performer often makes mistakes, we will restrict access to all our projects.

            >>> new_restriction = toloka_client.set_user_restriction(
            >>>     toloka.user_restriction.ProjectUserRestriction(
            >>>         user_id='1',
            >>>         private_comment='Performer often makes mistakes',
            >>>         project_id='5'
            >>>     )
            >>> )
            ...
        """
        ...

    @overload
    def set_user_skill(self, request: SetUserSkillRequest) -> UserSkill:
        """Sets the skill value to the performer

        Args:
            request: To whom and what value of the skill to set.

        Returns:
            UserSkill: Сreated fact of skill installation.

        Example:
            >>> from decimal import *
            >>> toloka_client.set_user_skill(skill_id='1', user_id='1', value=Decimal(100))
            ...
        """
        ...

    @overload
    def set_user_skill(
        self,
        *,
        skill_id: Optional[str] = None,
        user_id: Optional[str] = None,
        value: Optional[Decimal] = None
    ) -> UserSkill:
        """Sets the skill value to the performer

        Args:
            request: To whom and what value of the skill to set.

        Returns:
            UserSkill: Сreated fact of skill installation.

        Example:
            >>> from decimal import *
            >>> toloka_client.set_user_skill(skill_id='1', user_id='1', value=Decimal(100))
            ...
        """
        ...

    def update_pool(
        self,
        pool_id: str,
        pool: Pool
    ) -> Pool:
        """Makes changes to the pool

        Args:
            pool_id: ID of the pool that will be changed.
            pool: A pool object with all the fields: those that will be updated and those that will not.

        Returns:
            Pool: Pool object with all fields.

        Example:
            >>> updated_pool = toloka_client.update_pool(pool_id=old_pool_id, pool=new_pool_object)
            ...
        """
        ...

    def update_project(
        self,
        project_id: str,
        project: Project
    ) -> Project:
        """Makes changes to the project

        Args:
            project_id: Project ID that will be changed.
            project: A project object with all the fields: those that will be updated and those that will not.

        Returns:
            Project: Project object with all fields.

        Example:
            >>> updated_project = toloka_client.update_project(project_id=old_project.id, project=new_project_object)
            ...
        """
        ...

    def update_skill(
        self,
        skill_id: str,
        skill: Skill
    ) -> Skill:
        """Makes changes to the skill

        Args:
            skill_id: ID of the training that will be changed.
            skill: A skill object with all the fields: those that will be updated and those that will not.

        Returns:
            Skill: Modified skill object with all fields.

        Example:
            >>> toloka_client.create_skill(skill_id=old_skill_id, skill=new_skill_object)
            ...
        """
        ...

    def update_training(
        self,
        training_id: str,
        training: Training
    ) -> Training:
        """Makes changes to the training

        Args:
            training_id: ID of the training that will be changed.
            training: A training object with all the fields: those that will be updated and those that will not.

        Returns:
            Training: Training object with all fields.

        Example:
            If you want to update any configurations of the existing training.

            >>> updated_training = toloka_client.update_training(training_id=old_training_id, training=new_training_object)
            ...
        """
        ...

    def upsert_webhook_subscriptions(self, subscriptions: List[WebhookSubscription]) -> WebhookSubscriptionBatchCreateResult:
        """Creates (upsert) many webhook-subscriptions.

        Args:
            subscriptions: List of webhook-subscriptions, that will be created.

        Returns:
            batch_create_results.WebhookSubscriptionBatchCreateResult: Result of subscriptions creation.
                Contains created subscriptions in `items` and problems in "validation_errors".

        Raises:
            ValidationApiError: If no subscriptions were created.

        Example:
            How to create several subscriptions.

            >>> created_result = toloka_client.upsert_webhook_subscriptions([
            >>>     {
            >>>         'webhook_url': 'https://awesome-requester.com/toloka-webhook',
            >>>         'event_type': toloka.webhook_subscription.WebhookSubscription.EventType.ASSIGNMENT_CREATED,
            >>>         'pool_id': '121212'
            >>>     },
            >>>     {
            >>>         'webhook_url': 'https://awesome-requester.com/toloka-webhook',
            >>>         'event_type': toloka.webhook_subscription.WebhookSubscription.EventType.POOL_CLOSED,
            >>>         'pool_id': '121212',
            >>>     }
            >>> ])
            >>> print(len(created_result.items))
            ...
        """
        ...

    def wait_operation(
        self,
        op: Operation,
        timeout: timedelta = ...
    ) -> Operation:
        """Waits for the operation to complete, and return it

        Args:
            op: ID of the operation.
            timeout: How long to wait. Defaults to 10 minutes.

        Raises:
            TimeoutError: Raises it if the timeout has expired and the operation is still not completed.

        Returns:
            Operation: Completed operation.

        Example:
            Waiting for the pool to close can be running in the background.

            >>> pool = toloka_client.get_pool(pool_id)
            >>> while not pool.is_closed():
            >>>     op = toloka_client.get_analytics([toloka.analytics_request.CompletionPercentagePoolAnalytics(subject_id=pool.id)])
            >>>     op = toloka_client.wait_operation(op)
            >>>     percentage = op.details['value'][0]['result']['value']
            >>>     print(
            >>>         f'   {datetime.datetime.now().strftime("%H:%M:%S")}     '
            >>>         f'Pool {pool.id} - {percentage}%'
            >>>         )
            >>>     time.sleep(60 * minutes_to_wait)
            >>>     pool = toloka_client.get_pool(pool.id)
            >>> print('Pool was closed.')
            ...
        """
        ...
