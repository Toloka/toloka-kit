from typing import Dict, List, Any

from . import actions  # noqa: F401
from . import base  # noqa: F401
from . import conditions  # noqa: F401
from . import data  # noqa: F401
from . import fields  # noqa: F401
from . import helpers  # noqa: F401
from . import layouts  # noqa: F401
from . import plugins  # noqa: F401
from . import view  # noqa: F401
from .base import BaseComponent, base_component_or
from ...primitives.base import BaseTolokaObject


class TemplateBuilder(BaseTolokaObject):

    view: BaseComponent
    plugins: List[BaseComponent]
    vars: Dict[str, base_component_or(Any)]
