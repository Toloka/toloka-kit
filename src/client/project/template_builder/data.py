from typing import Any

from .base import BaseComponent, ComponentType, base_component_or


class BaseData(BaseComponent):
    path: base_component_or(Any)
    default: base_component_or(Any)


class InputData(BaseData, spec_value=ComponentType.DATA_INPUT):
    pass


class InternalData(BaseData, spec_value=ComponentType.DATA_INTERNAL):
    pass


class LocalData(BaseData, spec_value=ComponentType.DATA_LOCAL):
    pass


class OutputData(BaseData, spec_value=ComponentType.DATA_OUTPUT):
    pass


class RelativeData(BaseData, spec_value=ComponentType.DATA_RELATIVE):
    pass
