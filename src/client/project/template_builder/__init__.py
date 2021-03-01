from typing import Dict, List, Any, Union, Tuple

from . import actions  # noqa: F401
from . import base  # noqa: F401
from . import conditions  # noqa: F401
from . import data  # noqa: F401
from . import fields  # noqa: F401
from . import helpers  # noqa: F401
from . import layouts  # noqa: F401
from . import plugins  # noqa: F401
from . import view  # noqa: F401
from .base import ComponentType, BaseComponent, base_component_or
from ..field_spec import FieldSpec, JsonSpec
from ...primitives.base import BaseTolokaObject
from ...util import traverse_dicts_recursively


class TemplateBuilder(BaseTolokaObject):

    view: BaseComponent
    plugins: List[BaseComponent]
    vars: Dict[str, base_component_or(Any)]


def get_input_and_output(tb_config: Union[dict, TemplateBuilder]) -> Tuple[Dict[str, FieldSpec], Dict[str, FieldSpec]]:
    input_spec = {}
    output_spec = {}

    if isinstance(tb_config, TemplateBuilder):
        tb_config = tb_config.unstructure()

    for obj in traverse_dicts_recursively(tb_config):
        if obj.get('type') == ComponentType.DATA_INPUT.value:
            input_spec[obj['path']] = JsonSpec()
        elif obj.get('type') == ComponentType.DATA_OUTPUT.value:
            output_spec[obj['path']] = JsonSpec()

    return input_spec, output_spec
