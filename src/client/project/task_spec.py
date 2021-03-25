__all__ = ['TaskSpec']
from typing import Dict

from .field_spec import FieldSpec
from .view_spec import ViewSpec
from ..primitives.base import BaseTolokaObject


class TaskSpec(BaseTolokaObject):
    """Parameters for input and output data and the task interface.

    Attributes:
        input_spec: The input data parameters for tasks. The complete list of parameters is shown in the
            Input and output data table.
        output_spec: Parameters for output data from the input fields. The complete list of parameters is
            shown in the Input and output data table.
        view_spec: Description of the task interface.
    """

    input_spec: Dict[str, FieldSpec]
    output_spec: Dict[str, FieldSpec]
    view_spec: ViewSpec
