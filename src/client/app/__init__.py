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
    """
    Attributes:
        code: String error code.
        message: Detailed description of the error.
        payload: Additional information about the error. May have different structure for different errors.
    """
    code: str
    message: str
    payload: Any


class AppProject(BaseTolokaObject):
    """An App project with the parameters that you specify when creating it. It will have the interface and quality
    control already pre-configured, decomposition done, and everything ready to use: all you need is to upload batches
    and send them for labeling.

    Attributes:
        app_id:
        parent_app_project_id:
        name:
        parameters:
        id:
        status: Project statuses for asynchronous creation. Allowed values:
            * CREATING
            * READY
            * ARCHIVE
            * ERROR
        created:
        item_price:
        errors:
    """

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
    """An example of a standard task that you want to solve using Toloka. Unlike project templates, you don't have to
    set up everything yourself.

    Attributes:
        id: ID of the App.
        name:
        image: Image.
        description: Overview.
        constraints_description: Description of limitations.
        default_item_price: Default processing cost per work item.
        param_spec: Specification of parameters for creating a project.
        input_spec: Schema of input data in Toloka format.
        output_spec: Schema of output data in Toloka format.
        examples: Task examples.
    """

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
    """A work item with data. It's uploaded into the batch with other items to be collectively sent for labeling.
    In a TSV file with tasks, each line is a work item.

    Attributes:
        batch_id: ID of the batch that includes the item.
        input_data: The item data following the App schema.
        id: Item ID.
        app_project_id: ID of the app project that includes the batch with this item.
        created:
        updated:
        status: Processing status. If the item has the NEW status, it can be edited. In other statuses, the item is
            immutable. Allowed values:
            * NEW - new;
            * PROCESSING - being processed;
            * COMPLETED - processing complete;
            * ERROR - error during processing;
            * CANCELLED - processing canceled;
            * ARCHIVE - item has been archived;
            * NO_MONEY - not enough money for processing.
        output_data: Processing result.
        errors:
        created_at: Date and time when the item was created.
        started_at: Date and time when the item processing started.
        finished_at: Date and time when the item processing was completed.
    """

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
    updated: datetime.datetime = attribute(readonly=True)
    status: Status = attribute(readonly=True, autocast=True)
    output_data: Dict[str, Any] = attribute(readonly=True)
    errors: _AppError = attribute(readonly=True)
    created_at: datetime.datetime = attribute(readonly=True)
    started_at: datetime.datetime = attribute(readonly=True)
    finished_at: datetime.datetime = attribute(readonly=True)


class AppItemsCreateRequest(BaseTolokaObject):
    """Request Body.

    Attributes:
        batch_id: Batch ID.
        items: list of items.
    """

    batch_id: str
    items: List[Dict[str, Any]]


class AppBatch(BaseTolokaObject):
    """A batch of data that you send for labeling at a time. The batch consists of work items.

    Attributes:
        id: Batch ID.
        app_project_id: Project ID.
        name:
        status: The state of the batch, calculated based on the states of items comprising it. Allowed values:
            * NEW
            * PROCESSING
            * COMPLETED
            * ERROR
            * CANCELLED
            * ARCHIVE
            * NO_MONEY
        items_count: Number of items in the batch.
        item_price: The cost of processing per item in a batch.
        cost: The cost of processing per batch.
        created_at: Date and time when the batch was created.
        started_at: Date and time when batch processing started.
        finished_at: Date and time when batch processing was completed.
    """

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
    """Request Body.

    Attributes:
        items: The item data following the App schema.
    """

    items: List[Dict[str, Any]]
