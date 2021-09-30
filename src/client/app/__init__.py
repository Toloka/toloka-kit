__all__ = [
    'AppProject',
    'App',
    'AppItem',
    'AppItemsCreateRequest',
    'AppBatch',
    'AppBatchCreateRequest'
]
import datetime
import decimal
from enum import unique
from typing import Dict, Any, List

from ..primitives.base import BaseTolokaObject
from ..project.field_spec import FieldSpec
from ...util._extendable_enum import ExtendableStrEnum
from ...util._codegen import attribute


class _AppError(BaseTolokaObject):
    code: str
    message: str
    payload: Any


class AppProject(BaseTolokaObject):

    @unique
    class Status(ExtendableStrEnum):
        CREATING = 'CREATING'
        READY = 'READY'
        ARCHIVED = 'ARCHIVED'
        ERROR = 'ERROR'

    app_id: str
    parent_app_project_id: str
    name: str
    parameters: Dict

    id: str = attribute(readonly=True)
    status: Status = attribute(readonly=True, autocast=True)
    created: datetime.datetime = attribute(readonly=True)
    item_price: decimal.Decimal = attribute(readonly=True)
    errors: List[_AppError] = attribute(readonly=True)


class App(BaseTolokaObject):
    id: str
    name: str
    image: str
    description: str
    constraints_description: str
    default_item_price: decimal.Decimal
    param_spec: Dict
    input_spec: Dict[str, FieldSpec]
    output_spec: Dict[str, FieldSpec]
    examples: Any


class AppItem(BaseTolokaObject):

    @unique
    class Status(ExtendableStrEnum):
        NEW = 'NEW'
        PROCESSING = 'PROCESSING'
        COMPLETED = 'COMPLETED'
        ERROR = 'ERROR'
        CANCELLED = 'CANCELLED'
        ARCHIVE = 'ARCHIVE'
        NO_MONEY = 'NO_MONEY'

    batch_id: str
    input_data: Dict[str, Any]

    id: str = attribute(readonly=True)
    app_project_id: str = attribute(readonly=True)
    created: datetime.datetime = attribute(readonly=True)
    update: datetime.datetime = attribute(readonly=True)
    status: Status = attribute(readonly=True, autocast=True)
    output_data: Dict[str, Any] = attribute(readonly=True)
    errors: _AppError = attribute(readonly=True)
    created_at: datetime.datetime = attribute(readonly=True)
    started_at: datetime.datetime = attribute(readonly=True)
    finished_at: datetime.datetime = attribute(readonly=True)


class AppItemsCreateRequest(BaseTolokaObject):

    batch_id: str
    items: List[Dict[str, Any]]


class AppBatch(BaseTolokaObject):

    @unique
    class Status(ExtendableStrEnum):
        NEW = 'NEW'
        PROCESSING = 'PROCESSING'
        COMPLETED = 'COMPLETED'
        ERROR = 'ERROR'
        CANCELLED = 'CANCELLED'
        ARCHIVE = 'ARCHIVE'
        NO_MONEY = 'NO_MONEY'

    id: str
    app_project_id: str
    name: str
    status: Status = attribute(autocast=True)
    items_count: int
    item_price: decimal.Decimal
    cost: decimal.Decimal
    created_at: datetime.datetime
    started_at: datetime.datetime
    finished_at: datetime.datetime


class AppBatchCreateRequest(BaseTolokaObject):

    items: List[Dict[str, Any]]
