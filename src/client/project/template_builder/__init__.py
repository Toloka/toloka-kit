__all__ = [
    'TemplateBuilder',
    'get_input_and_output',
    'BulkActionV1',
    'NotifyActionV1',
    'OpenCloseActionV1',
    'OpenLinkActionV1',
    'PlayPauseActionV1',
    'RotateActionV1',
    'SetActionV1',
    'ToggleActionV1',
    'AllConditionV1',
    'AnyConditionV1',
    'EmptyConditionV1',
    'EqualsConditionV1',
    'LinkOpenedConditionV1',
    'NotConditionV1',
    'PlayedConditionV1',
    'PlayedFullyConditionV1',
    'RequiredConditionV1',
    'SchemaConditionV1',
    'SubArrayConditionV1',
    'InputData',
    'InternalData',
    'LocalData',
    'OutputData',
    'RelativeData',
    'ButtonRadioFieldV1',
    'GroupFieldOption',
    'ButtonRadioGroupFieldV1',
    'CheckboxFieldV1',
    'CheckboxGroupFieldV1',
    'DateFieldV1',
    'EmailFieldV1',
    'FileFieldV1',
    'ImageAnnotationFieldV1',
    'ListFieldV1',
    'MediaFileFieldV1',
    'NumberFieldV1',
    'PhoneNumberFieldV1',
    'RadioGroupFieldV1',
    'SelectFieldV1',
    'TextFieldV1',
    'TextareaFieldV1',
    'ConcatArraysHelperV1',
    'Entries2ObjectHelperV1',
    'IfHelperV1',
    'JoinHelperV1',
    'Object2EntriesHelperV1',
    'ReplaceHelperV1',
    'SearchQueryHelperV1',
    'SwitchHelperV1',
    'TextTransformHelperV1',
    'TransformHelperV1',
    'YandexDiskProxyHelperV1',
    'BarsLayoutV1',
    'ColumnsLayoutV1',
    'SideBySideLayoutV1',
    'SidebarLayoutV1',
    'HotkeysPluginV1',
    'TriggerPluginV1',
    'TolokaPluginV1',
    'ActionButtonViewV1',
    'AlertViewV1',
    'AudioViewV1',
    'CollapseViewV1',
    'DeviceFrameViewV1',
    'DividerViewV1',
    'GroupViewV1',
    'IframeViewV1',
    'ImageViewV1',
    'LabeledListViewV1',
    'LinkViewV1',
    'ListViewV1',
    'MarkdownViewV1',
    'TextViewV1',
    'VideoViewV1',
]
from typing import Dict, List, Any, Union, Tuple

from .actions import (
    BulkActionV1,
    NotifyActionV1,
    OpenCloseActionV1,
    OpenLinkActionV1,
    PlayPauseActionV1,
    RotateActionV1,
    SetActionV1,
    ToggleActionV1,
)
from .conditions import (
    AllConditionV1,
    AnyConditionV1,
    EmptyConditionV1,
    EqualsConditionV1,
    LinkOpenedConditionV1,
    NotConditionV1,
    PlayedConditionV1,
    PlayedFullyConditionV1,
    RequiredConditionV1,
    SchemaConditionV1,
    SubArrayConditionV1,
)
from .data import (
    InputData,
    InternalData,
    LocalData,
    OutputData,
    RelativeData,
)
from .fields import (
    ButtonRadioFieldV1,
    GroupFieldOption,
    ButtonRadioGroupFieldV1,
    CheckboxFieldV1,
    CheckboxGroupFieldV1,
    DateFieldV1,
    EmailFieldV1,
    FileFieldV1,
    ImageAnnotationFieldV1,
    ListFieldV1,
    MediaFileFieldV1,
    NumberFieldV1,
    PhoneNumberFieldV1,
    RadioGroupFieldV1,
    SelectFieldV1,
    TextFieldV1,
    TextareaFieldV1,
)
from .helpers import (
    ConcatArraysHelperV1,
    Entries2ObjectHelperV1,
    IfHelperV1,
    JoinHelperV1,
    Object2EntriesHelperV1,
    ReplaceHelperV1,
    SearchQueryHelperV1,
    SwitchHelperV1,
    TextTransformHelperV1,
    TransformHelperV1,
    YandexDiskProxyHelperV1,
)
from .layouts import (
    BarsLayoutV1,
    ColumnsLayoutV1,
    SideBySideLayoutV1,
    SidebarLayoutV1,
)
from .plugins import (
    HotkeysPluginV1,
    TriggerPluginV1,
    TolokaPluginV1,
)
from .view import (
    ActionButtonViewV1,
    AlertViewV1,
    AudioViewV1,
    CollapseViewV1,
    DeviceFrameViewV1,
    DividerViewV1,
    GroupViewV1,
    IframeViewV1,
    ImageViewV1,
    LabeledListViewV1,
    LinkViewV1,
    ListViewV1,
    MarkdownViewV1,
    TextViewV1,
    VideoViewV1,
)
from .base import ComponentType, BaseComponent, base_component_or
from ..field_spec import FieldSpec, JsonSpec
from ...primitives.base import BaseTolokaObject
from ...util import traverse_dicts_recursively


class TemplateBuilder(BaseTolokaObject):

    view: BaseComponent  # noqa: F811
    plugins: List[BaseComponent]  # noqa: F811
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
