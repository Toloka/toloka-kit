import datetime
from enum import Enum, unique
from typing import Any, ClassVar

from .primitives.base import BaseTolokaObject


@unique
class OperationType(Enum):
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

    @unique
    class Status(Enum):
        PENDING = 'PENDING'
        RUNNING = 'RUNNING'
        SUCCESS = 'SUCCESS'
        FAIL = 'FAIL'

    PENDING = Status.PENDING
    RUNNING = Status.RUNNING
    SUCCESS = Status.SUCCESS
    FAIL = Status.FAIL

    class Parameters(BaseTolokaObject):
        pass

    PSEUDO_OPERATION_ID: ClassVar[str] = 'PSEUDO_ID'
    DEFAULT_PSEUDO_OPERATION_TYPE: ClassVar[OperationType] = OperationType.PSEUDO

    id: str
    status: Status
    submitted: datetime.datetime
    parameters: Parameters
    started: datetime.datetime
    finished: datetime.datetime
    progress: int
    details: Any  # TODO: cannot structure dict.

    def is_completed(self):
        return self.status in [Operation.Status.SUCCESS, Operation.Status.FAIL]


# Analytics operations


class AnalyticsOperation(Operation, spec_value=OperationType.ANALYTICS):
    pass


# Pool operations


class PoolOperation(Operation):

    class Parameters(Operation.Parameters):
        pool_id: str

    parameters: Parameters


class PoolArchiveOperation(PoolOperation, spec_value=OperationType.POOL_ARCHIVE):
    pass


class PoolCloneOperation(PoolOperation, spec_value=OperationType.POOL_CLONE):

    class Details(PoolOperation.Parameters):
        pool_id: str

    details: Details


class PoolCloseOperation(PoolOperation, spec_value=OperationType.POOL_CLOSE):
    pass


class PoolOpenOperation(PoolOperation, spec_value=OperationType.POOL_OPEN):
    pass


# Training operations


class TrainingOperation(Operation):

    class Parameters(Operation.Parameters):
        training_id: str

    parameters: Parameters


class TrainingArchiveOperation(TrainingOperation, spec_value=OperationType.TRAINING_ARCHIVE):
    pass


class TrainingCloneOperation(TrainingOperation, spec_value=OperationType.TRAINING_CLONE):

    class Details(TrainingOperation.Parameters):
        training_id: str

    details: Details


class TrainingCloseOperation(TrainingOperation, spec_value=OperationType.TRAINING_CLOSE):
    pass


class TrainingOpenOperation(TrainingOperation, spec_value=OperationType.TRAINING_OPEN):
    pass


# Project operations


class ProjectArchiveOperation(Operation, spec_value=OperationType.PROJECT_ARCHIVE):

    class Parameters(Operation.Parameters):
        project_id: str

    parameters: Parameters


# Task operations


class TasksCreateOperation(Operation, spec_value=OperationType.TASK_BATCH_CREATE):

    class Parameters(Operation.Parameters):
        skip_invalid_items: bool
        allow_defaults: bool
        open_pool: bool

    parameters: Parameters
    finished: datetime.datetime
    details: Any


# TaskSuit operations


class TaskSuiteCreateBatchOperation(Operation, spec_value=OperationType.TASK_SUITE_BATCH_CREATE):

    class Parameters(Operation.Parameters):
        skip_invalid_items: bool
        allow_defaults: bool
        open_pool: bool

    parameters: Parameters
    finished: datetime.datetime
    details: Any


# Aggregation


class AggregatedSolutionOperation(Operation, spec_value=OperationType.SOLUTION_AGGREGATE):

    class Parameters(Operation.Parameters):
        pool_id: str

    parameters: Parameters


# UserBonus


class UserBonusCreateBatchOperation(Operation, spec_value=OperationType.USER_BONUS_BATCH_CREATE):

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
