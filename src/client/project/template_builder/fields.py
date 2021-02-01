from typing import List, Any

from ...primitives.base import attribute

from .base import BaseComponent, ListDirection, ListSize, ComponentType, BaseTemplate, VersionedBaseComponent,\
    base_component_or


class BaseFieldV1(VersionedBaseComponent):
    data: BaseComponent
    hint: base_component_or(Any)
    label: base_component_or(Any)
    validation: BaseComponent


class ButtonRadioFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_BUTTON_RADIO):
    value_to_set: base_component_or(Any) = attribute(origin='valueToSet')


class GroupFieldOption(BaseTemplate):
    label: base_component_or(Any)
    value: base_component_or(Any)
    hint: base_component_or(Any)


class ButtonRadioGroupFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_BUTTON_RADIO_GROUP):
    options: base_component_or(List[base_component_or(GroupFieldOption)], 'ListBaseComponentOrGroupFieldOption')


class CheckboxFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_CHECKBOX):
    disabled: base_component_or(bool)
    preserve_false: base_component_or(bool) = attribute(origin='preserveFalse')


class CheckboxGroupFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_CHECKBOX_GROUP):
    options: base_component_or(List[base_component_or(GroupFieldOption)], 'ListBaseComponentOrGroupFieldOption')
    disabled: base_component_or(bool)
    preserve_false: base_component_or(bool) = attribute(origin='preserveFalse')


class DateFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_DATE):
    format: base_component_or(Any)
    block_list: base_component_or(List[base_component_or(Any)], 'ListBaseComponentOrAny') = attribute(origin='')
    max: base_component_or(Any)
    min: base_component_or(Any)
    placeholder: base_component_or(Any)


class ListFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_LIST):
    render: BaseComponent
    button_label: base_component_or(Any)
    direction: base_component_or(ListDirection)
    editable: base_component_or(Any)
    max_length: base_component_or(float)
    size: base_component_or(ListSize)


class NumberFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_NUMBER):
    maximum: base_component_or(int)
    minimum: base_component_or(int)
    placeholder: base_component_or(Any)


class RadioGroupFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_RADIO_GROUP):
    options: base_component_or(List[base_component_or(GroupFieldOption)], 'ListBaseComponentOrGroupFieldOption')
    disabled: base_component_or(bool)


class SelectFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_SELECT):

    class Option(BaseTemplate):
        label: base_component_or(Any)
        value: base_component_or(Any)

    options: base_component_or(Option)
    placeholder: base_component_or(Any)


class TextFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_TEXT):
    disabled: base_component_or(bool)
    placeholder: base_component_or(Any)


class TextareaFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_TEXTAREA):
    disabled: base_component_or(bool)
    placeholder: base_component_or(Any)
    resizable: base_component_or(bool)
    rows: base_component_or(float)
