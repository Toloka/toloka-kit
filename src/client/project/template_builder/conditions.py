from typing import List, Any, Dict

from .base import BaseComponent, ComponentType, VersionedBaseComponent, base_component_or


class BaseConditionV1(VersionedBaseComponent):
    hint: base_component_or(Any)


class AllConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_ALL):
    conditions: base_component_or(List[BaseComponent], 'ListBaseComponent')


class AnyConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_ANY):
    conditions: base_component_or(List[BaseComponent], 'ListBaseComponent')


class EmptyConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_EMPTY):
    data: base_component_or(Any)


class EqualsConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_EQUALS):
    to: base_component_or(Any)
    data: base_component_or(Any)


class LinkOpenedConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_LINK_OPENED):
    url: base_component_or(Any)


class NotConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_NOT):
    condition: BaseComponent


class PlayedConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_PLAYED):
    pass


class PlayedFullyConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_PLAYED_FULLY):
    pass


class RequiredConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_REQUIRED):
    data: base_component_or(Any)


class SchemaConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_SCHEMA):
    data: base_component_or(Any)
    schema: Dict  # TODO: support base_component_or(Dict)


class SubArrayConditionV1(BaseConditionV1, spec_value=ComponentType.CONDITION_SUB_ARRAY):
    data: base_component_or(Any)
    parent: base_component_or(Any)
