from typing import Dict

from .field_spec import FieldSpec
from .view_spec import ViewSpec
from ..primitives.base import BaseTolokaObject


class TaskSpec(BaseTolokaObject):
    input_spec: Dict[str, FieldSpec]
    output_spec: Dict[str, FieldSpec]
    view_spec: ViewSpec
