__all__ = ['TaskSpec']
from typing import Dict

from .field_spec import FieldSpec
from .view_spec import ViewSpec
from ..primitives.base import BaseTolokaObject


class TaskSpec(BaseTolokaObject):
    """Task interface description and input and output data specification.

    Attributes:
        input_spec: The input data parameters for tasks.
        output_spec: Parameters for output data from the input fields. The complete list of parameters is
            shown in the Input and output data table.
        view_spec: Description of the task interface.
    """

    input_spec: Dict[str, FieldSpec]
    output_spec: Dict[str, FieldSpec]
    view_spec: ViewSpec
