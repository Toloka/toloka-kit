from enum import Enum, unique
from typing import List, Any

from ...primitives.base import attribute

from .base import BaseTemplate, BaseComponent, ListDirection, ListSize, ComponentType, VersionedBaseComponent, base_component_or


class BaseViewV1(VersionedBaseComponent):
    hint: base_component_or(Any)
    label: base_component_or(Any)
    validation: BaseComponent


class ActionButtonViewV1(BaseViewV1, spec_value=ComponentType.VIEW_ACTION_BUTTON):
    action: BaseComponent


class AlertViewV1(BaseViewV1, spec_value=ComponentType.VIEW_ALERT):

    @unique
    class Theme(Enum):
        DANGER = 'danger'
        INFO = 'info'
        SUCCESS = 'success'
        WARNING = 'warning'

    content: BaseComponent
    theme: base_component_or(Theme)


class AudioViewV1(BaseViewV1, spec_value=ComponentType.VIEW_AUDIO):
    url: base_component_or(Any)
    loop: base_component_or(bool)


class CollapseViewV1(BaseViewV1, spec_value=ComponentType.VIEW_COLLAPSE):
    content: BaseComponent
    default_opened: base_component_or(bool) = attribute(origin='defaultOpened')


class DeviceFrameViewV1(BaseViewV1, spec_value=ComponentType.VIEW_DEVICE_FRAME):
    content: BaseComponent
    full_height: base_component_or(bool) = attribute(origin='fullHeight')
    max_width: base_component_or(float) = attribute(origin='maxWidth')
    min_width: base_component_or(float) = attribute(origin='minWidth')
    ratio: base_component_or(List[base_component_or(float)], 'ListBaseComponentOrFloat')


class DividerViewV1(BaseViewV1, spec_value=ComponentType.VIEW_DIVIDER):
    pass


class GroupViewV1(BaseViewV1, spec_value=ComponentType.VIEW_GROUP):
    content: BaseComponent


class IframeViewV1(BaseViewV1, spec_value=ComponentType.VIEW_IFRAME):
    url: base_component_or(str)
    full_height: base_component_or(bool) = attribute(origin='fullHeight')
    max_width: base_component_or(float) = attribute(origin='maxWidth')
    min_width: base_component_or(float) = attribute(origin='minWidth')
    ratio: base_component_or(List[base_component_or(float)], 'ListBaseComponentOrFloat')


class ImageViewV1(BaseViewV1, spec_value=ComponentType.VIEW_IMAGE):
    url: base_component_or(Any)
    full_height: base_component_or(bool) = attribute(origin='fullHeight')
    max_width: base_component_or(float) = attribute(origin='maxWidth')
    min_width: base_component_or(float) = attribute(origin='minWidth')
    no_border: base_component_or(bool) = attribute(origin='noBorder')
    no_lazy_load: base_component_or(bool) = attribute(origin='noLazyLoad')
    popup: base_component_or(bool)
    ratio: base_component_or(List[base_component_or(float)], 'ListBaseComponentOrFloat')
    rotatable: base_component_or(bool)
    scrollable: base_component_or(bool)


class LabeledListViewV1(BaseViewV1, spec_value=ComponentType.VIEW_LABELED_LIST):

    class Item(BaseTemplate):
        content: BaseComponent
        label: base_component_or(Any)
        center_label: base_component_or(bool) = attribute(origin='centerLabel')
        hint: base_component_or(Any)

    items: base_component_or(List[base_component_or(Item)], 'ListBaseComponentOrItem')
    min_width: base_component_or(float) = attribute(origin='minWidth')


class LinkViewV1(BaseViewV1, spec_value=ComponentType.VIEW_LINK):
    url: base_component_or(Any)
    content: base_component_or(Any)


class ListViewV1(BaseViewV1, spec_value=ComponentType.VIEW_LIST):
    items: base_component_or(List[BaseComponent], 'ListBaseComponent')
    direction: base_component_or(ListDirection)
    size: base_component_or(ListSize)


class MarkdownViewV1(BaseViewV1, spec_value=ComponentType.VIEW_MARKDOWN):
    content: base_component_or(Any)


class TextViewV1(BaseViewV1, spec_value=ComponentType.VIEW_TEXT):
    content: base_component_or(Any)


class VideoViewV1(BaseViewV1, spec_value=ComponentType.VIEW_VIDEO):
    full_height: base_component_or(bool) = attribute(origin='fullHeight')
    max_width: base_component_or(float) = attribute(origin='maxWidth')
    min_width: base_component_or(float) = attribute(origin='minWidth')
