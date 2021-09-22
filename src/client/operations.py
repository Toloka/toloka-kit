__all__ = [
    'OperationType',
    'Operation',
    'AnalyticsOperation',
    'PoolOperation',
    'PoolArchiveOperation',
    'PoolCloneOperation',
    'PoolCloseOperation',
    'PoolOpenOperation',
    'TrainingOperation',
    'TrainingArchiveOperation',
    'TrainingCloneOperation',
    'TrainingCloseOperation',
    'TrainingOpenOperation',
    'ProjectArchiveOperation',
    'TasksCreateOperation',
    'TaskSuiteCreateBatchOperation',
    'AggregatedSolutionOperation',
    'UserBonusCreateBatchOperation'
]
import datetime
from enum import unique
from typing import Any, ClassVar

from .exceptions import FailedOperation
from .primitives.base import BaseTolokaObject
from ..util._codegen import attribute
from ..util._docstrings import inherit_docstrings
from ..util._extendable_enum import ExtendableStrEnum


@unique
class OperationType(ExtendableStrEnum):
    PSEUDO = 'PSEUDO.PSEUDO'
    PROJECT_ARCHIVE = 'PROJECT.ARCHIVE'
    POOL_OPEN = 'POOL.OPEN'
    POOL_CLOSE = 'POOL.CLOSE'
    POOL_ARCHIVE = 'POOL.ARCHIVE'
    POOL_CLONE = 'POOL.CLONE'
    TRAINING_OPEN = 'TRAINING.OPEN'
    TRAINING_CLOSE = 'TRAINING.CLOSE'
    TRAINING_ARCHIVE = 'TRAINING.ARCHIVE'
    TRAINING_CLONE = 'TRAINING.CLONE'
    TASK_BATCH_CREATE = 'TASK.BATCH_CREATE'
    TASK_SUITE_BATCH_CREATE = 'TASK_SUITE.BATCH_CREATE'
    USER_BONUS_BATCH_CREATE = 'USER_BONUS.BATCH_CREATE'
    ANALYTICS = 'ANALYTICS'
    SOLUTION_AGGREGATE = 'SOLUTION.AGGREGATE'


class Operation(BaseTolokaObject, spec_enum=OperationType, spec_field='type'):
    """Tracking Operation

    Some API requests (opening and closing a pool, archiving a pool or a project, loading multiple tasks,
    awarding bonuses) are processed as asynchronous operations that run in the background.

    Attributes:
        id: Operation ID.
        status: The status of the operation.
        submitted: The UTC date and time the request was sent.
        parameters: Operation parameters (depending on the operation type).
        started: The UTC date and time the operation started.
        finished: The UTC date and time the operation finished.
        progress: The percentage of the operation completed.
        details: Details of the operation completion.
    """

    @unique
    class Status(ExtendableStrEnum):
        """The status of the operation:

        Attributes:
            PENDING: Not started yet.
            RUNNING: In progress.
            SUCCESS: Completed successfully.
            FAIL: Not completed.
        """

        PENDING = 'PENDING'
        RUNNING = 'RUNNING'
        SUCCESS = 'SUCCESS'
        FAIL = 'FAIL'

    PENDING = Status.PENDING
    RUNNING = Status.RUNNING
    SUCCESS = Status.SUCCESS
    FAIL = Status.FAIL

    class Parameters(BaseTolokaObject):
        """Operation parameters (depending on the operation type).

        """

        pass

    PSEUDO_OPERATION_ID: ClassVar[str] = 'PSEUDO_ID'
    DEFAULT_PSEUDO_OPERATION_TYPE: ClassVar[OperationType] = OperationType.PSEUDO

    id: str
    status: Status = attribute(autocast=True)
    submitted: datetime.datetime
    parameters: Parameters
    started: datetime.datetime
    finished: datetime.datetime
    progress: int
    details: Any  # TODO: cannot structure dict.

    def is_completed(self):
        """Returns True if the operation is completed. Status equals SUCCESS or FAIL."""
        return self.status in [Operation.Status.SUCCESS, Operation.Status.FAIL]

    def raise_on_fail(self):
        """Raises FailedOperation exception if status is FAIL. Otherwise does nothing."""
        if self.status == Operation.Status.FAIL:
            raise FailedOperation(operation=self)


# Analytics operations


@inherit_docstrings
class AnalyticsOperation(Operation, spec_value=OperationType.ANALYTICS):
    """Operation returned when requesting analytics via TolokaClient.get_analytics()
    """

    pass


# Pool operations


@inherit_docstrings
class PoolOperation(Operation):
    """Base class for all operations on pool

    Attributes:
        parameters.pool_id: On which pool operation is performed.
    """

    class Parameters(Operation.Parameters):
        pool_id: str

    parameters: Parameters


@inherit_docstrings
class PoolArchiveOperation(PoolOperation, spec_value=OperationType.POOL_ARCHIVE):
    """Operation returned by an asynchronous archive pool via TolokaClient.archive_pool_async()
    """

    pass


@inherit_docstrings
class PoolCloneOperation(PoolOperation, spec_value=OperationType.POOL_CLONE):
    """Operation returned by an asynchronous cloning pool via TolokaClient.clone_pool_async()

    As parameters.pool_id contains id of the pool that needs to be cloned.
    New pool id stored in details.pool_id.
    Don't be mistaken.

    Attributes:
        details.pool_id: New pool id created after cloning.
    """

    class Details(PoolOperation.Parameters):
        pool_id: str

    details: Details


@inherit_docstrings
class PoolCloseOperation(PoolOperation, spec_value=OperationType.POOL_CLOSE):
    """Operation returned by an asynchronous closing pool via TolokaClient.close_pool_async()
    """

    pass


@inherit_docstrings
class PoolOpenOperation(PoolOperation, spec_value=OperationType.POOL_OPEN):
    """Operation returned by an asynchronous opening pool via TolokaClient.open_pool_async()
    """

    pass


# Training operations


@inherit_docstrings
class TrainingOperation(Operation):
    """Base class for all operations on training pool

    Attributes:
        parameters.training_id: On which training pool operation is performed.
    """

    class Parameters(Operation.Parameters):
        training_id: str

    parameters: Parameters


@inherit_docstrings
class TrainingArchiveOperation(TrainingOperation, spec_value=OperationType.TRAINING_ARCHIVE):
    """Operation returned by an asynchronous archive training pool via TolokaClient.archive_training_async()
    """

    pass


@inherit_docstrings
class TrainingCloneOperation(TrainingOperation, spec_value=OperationType.TRAINING_CLONE):
    """Operation returned by an asynchronous cloning training pool via TolokaClient.clone_training_async()

    As parameters.training_id contains id of the training pool that needs to be cloned.
    New training pool id stored in details.training_id.
    Don't be mistaken.

    Attributes:
        details.pool_id: New training pool id created after cloning.
    """

    class Details(TrainingOperation.Parameters):
        training_id: str

    details: Details


@inherit_docstrings
class TrainingCloseOperation(TrainingOperation, spec_value=OperationType.TRAINING_CLOSE):
    """Operation returned by an asynchronous closing training pool via TolokaClient.close_training_async()
    """

    pass


@inherit_docstrings
class TrainingOpenOperation(TrainingOperation, spec_value=OperationType.TRAINING_OPEN):
    """Operation returned by an asynchronous opening training pool via TolokaClient.open_training_async()
    """

    pass


# Project operations


@inherit_docstrings
class ProjectArchiveOperation(Operation, spec_value=OperationType.PROJECT_ARCHIVE):
    """Operation returned by an asynchronous archive project via TolokaClient.archive_project_async()

    Attributes:
        parameters.project_id: On which project operation is performed.
    """

    class Parameters(Operation.Parameters):
        project_id: str

    parameters: Parameters


# Task operations


@inherit_docstrings
class TasksCreateOperation(Operation, spec_value=OperationType.TASK_BATCH_CREATE):
    """Operation returned by an asynchronous creating tasks via TolokaClient.create_tasks_async()

    All parameters are for reference only and describe the initial parameters of the request that this operation monitors.

    Attributes:
        parameters.skip_invalid_items: Validation parameters for JSON objects:
            * True - Create the tasks that passed validation. Skip the rest of the tasks.
            * False - If at least one of the tasks didn't pass validation, stop the operation and
                don't create any tasks.
        parameters.allow_defaults: Overlap settings:
            * True - Use the overlap that is set in the pool parameters
                (in the defaults.default_overlap_for_new_tasks key).
            * False - Use the overlap that is set in the task parameters (in the overlap field).
        parameters.open_pool: Open the pool immediately after creating the tasks, if the pool is closed.
    """

    class Parameters(Operation.Parameters):
        skip_invalid_items: bool
        allow_defaults: bool
        open_pool: bool

    parameters: Parameters
    finished: datetime.datetime
    details: Any


# TaskSuit operations


@inherit_docstrings
class TaskSuiteCreateBatchOperation(Operation, spec_value=OperationType.TASK_SUITE_BATCH_CREATE):
    """Operation returned by an asynchronous creating TaskSuite's via TolokaClient.create_task_suites_async()

    All parameters are for reference only and describe the initial parameters of the request that this operation monitors.

    Attributes:
        parameters.skip_invalid_items: Validation parameters for JSON objects:
            * True - Create the task suites that passed validation. Skip the rest of the task suites.
            * False - If at least one of the task suites didn't pass validation, stop the operation and
                don't create any task suites.
        parameters.allow_defaults: Overlap settings:
            * True - Use the overlap that is set in the pool parameters.
            * False - Use the overlap that is set in the task parameters (in the overlap field).
        parameters.open_pool: Open the pool immediately after creating the task suites, if the pool is closed.
    """

    class Parameters(Operation.Parameters):
        skip_invalid_items: bool
        allow_defaults: bool
        open_pool: bool

    parameters: Parameters
    finished: datetime.datetime
    details: Any


# Aggregation


@inherit_docstrings
class AggregatedSolutionOperation(Operation, spec_value=OperationType.SOLUTION_AGGREGATE):
    """Operation returned by an asynchronous aggregation responses in pool via TolokaClient.aggregate_solutions_by_pool()

    Attributes:
        parameters.pool_id: In which pool the responses are aggregated.
    """

    class Parameters(Operation.Parameters):
        pool_id: str

    parameters: Parameters


# UserBonus


@inherit_docstrings
class UserBonusCreateBatchOperation(Operation, spec_value=OperationType.USER_BONUS_BATCH_CREATE):
    """Operation returned by an asynchronous creating user bonuses via TolokaClient.create_user_bonuses_async()

    All parameters are for reference only and describe the initial parameters of the request that this operation monitors.

    Attributes:
        parameters.skip_invalid_items: Validation parameters for JSON objects:
            * True - Create the user bonuses that passed validation. Skip the rest of the user bonuses.
            * False - If at least one of the user bonus didn't pass validation, stop the operation and
                don't create any user bonus.
        details.pool_id:
        details.total_count: The number of bonuses in the request.
        details.valid_count: The number of JSON objects with bonus information that have passed validation.
        details.not_valid_count: The number of JSON objects with bonus information that failed validation.
        details.success_count: Number of bonuses issued.
        details.failed_count: The number of bonuses that were not issued.
    """

    class Parameters(Operation.Parameters):
        skip_invalid_items: bool

    class Details(PoolOperation.Parameters):
        total_count: int
        valid_count: int
        not_valid_count: int
        success_count: int
        failed_count: int

    parameters: Parameters
    details: Details
