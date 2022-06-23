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
    A structure for describing errors which may appear while working with ready-to-go solutions.

    Attributes:
        code: The short name of the error.
        message: The detailed description of the error.
        payload: Additional data provided with the error.
    """
    code: str
    message: str
    payload: Any


class AppProject(BaseTolokaObject):
    """A [ready-to-go](https://toloka.ai/en/docs/toloka-apps/concepts/) project.
    
    A ready-to-go project is based on one of ready-to-go solutions. It is created with a template interface and preconfigured data specification and quality control rules.

    To get available ready-to-go solutions use the [get_apps](toloka.client.TolokaClient.get_apps.md) method.

    Attributes:
        app_id: The ID of the ready-to-go solution used to create the project.
        parent_app_project_id The ID of the parent project. It is set if this project is a clone of other project. Otherwise it is empty.
        name: The project name.
        parameters: Parameters of the solution. The parameters should follow a schema described in the `param_spec` field of the [App](toloka.client.app.App.md).
        id: The ID of the project.
        status: The project status:
            * `CREATING` — Toloka is checking the project.
            * `READY` — The project is active.
            * `ARCHIVED` — The project was archived.
            * `ERROR` — Project creation failed due to errors.
        created: Time when the project was created.
        item_price: The price you pay for a processed item.
        errors: Errors found during a project check.
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
    """A [ready-to-go](https://toloka.ai/en/docs/toloka-apps/concepts/) solution.
    
    Each ready-to-go solution targets one type of tasks which can be solved using Toloka. 

    Attributes:
        id: The ID of the ready-to-go solution.
        name: The solution name.
        image: A link to the solution interface preview image.
        description: The solution description.
        constraints_description: The description of limitations.
        default_item_price: The default cost of one annotated item.
        param_spec: The specification of parameters used to create a project.
        input_spec: The schema of solution input data.
        output_spec: The schema of solution output data.
        examples: Examples of tasks suitable to the solution.
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
    """A work item with data.
    
    Items are uploaded to Toloka and are grouped in batches. Then the entire batch is sent for labeling.

    Attributes:
        id: The ID of the item.
        app_project_id: The ID of the project that contains the item.
        batch_id: The ID of the batch that contains the item.
        input_data: Input data. It must follow the solution schema described in `App.input_spec`.
        created:
        updated: 
        status: A processing status. Only items in `NEW` status can be edited.
            * `NEW` — New item.
            * `PROCESSING` — The item is being processed.
            * `COMPLETED` — The item is annotated.
            * `ERROR` — An error occurred during processing.
            * `CANCELLED` — Item processing canceled.
            * `ARCHIVE` — Archived item.
            * `NO_MONEY` — There are not enough money for processing.
        output_data: Annotated data.
        errors: Errors occurred during annotation.
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
    errors: List[_AppError] = attribute(readonly=True)
    created_at: datetime.datetime = attribute(readonly=True)
    started_at: datetime.datetime = attribute(readonly=True)
    finished_at: datetime.datetime = attribute(readonly=True)


class AppItemsCreateRequest(BaseTolokaObject):
    """Parameters of a request for creating multiple items.

    Attributes:
        batch_id: The ID of the batch to place items to.
        items: The list of items. The items must follow the solution schema described in `App.input_spec`.
    """

    batch_id: str
    items: List[Dict[str, Any]]


class AppBatch(BaseTolokaObject):
    """A batch.
    
    A batch contains items that are sent for labeling together.

    Attributes:
        id: The ID of the Batch.
        app_project_id: The ID of the project.
        name: The batch name.
        status: The batch status:
            * `NEW`
            * `PROCESSING`
            * `COMPLETED`
            * `ERROR`
            * `CANCELLED`
            * `ARCHIVE`
            * `NO_MONEY`
        items_count: The number of items in the batch.
        item_price: The cost of processing single item.
        cost: The cost of processing the batch.
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
    """Parameters of a request for creating multiple items in a batch.

    Attributes:
        items: The list of items. The items must follow the solution schema described in `App.input_spec`.
    """

    items: List[Dict[str, Any]]
