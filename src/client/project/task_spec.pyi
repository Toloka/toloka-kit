from typing import Any, Dict, Optional

from ..primitives.base import BaseTolokaObject
from .field_spec import FieldSpec
from .view_spec import ViewSpec


class TaskSpec(BaseTolokaObject):
    """Parameters for input and output data and the task interface.

    Attributes:
        input_spec: The input data parameters for tasks. The complete list of parameters is shown in the
            Input and output data table.
        output_spec: Parameters for output data from the input fields. The complete list of parameters is
            shown in the Input and output data table.
        view_spec: Description of the task interface.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        input_spec: Optional[Dict[str, FieldSpec]] = ...,
        output_spec: Optional[Dict[str, FieldSpec]] = ...,
        view_spec: Optional[ViewSpec] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    input_spec: Optional[Dict[str, FieldSpec]]
    output_spec: Optional[Dict[str, FieldSpec]]
    view_spec: Optional[ViewSpec]
