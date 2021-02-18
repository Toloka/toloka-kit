from enum import Enum, unique
from typing import List

from ...primitives.base import attribute

from .base import BaseComponent, ComponentType, VersionedBaseComponent, base_component_or


class BaseLayoutV1(VersionedBaseComponent):
    validation: BaseComponent


class BarsLayoutV1(BaseLayoutV1, spec_value=ComponentType.LAYOUT_BARS):
    content: BaseComponent
    bar_after: BaseComponent = attribute(origin='barAfter')
    bar_before: BaseComponent = attribute(origin='barBefore')


class ColumnsLayoutV1(BaseLayoutV1, spec_value=ComponentType.LAYOUT_COLUMNS):

    @unique
    class VerticalAlign(Enum):
        BOTTOM = 'bottom'
        MIDDLE = 'middle'
        TOP = 'top'

    items: base_component_or(List[BaseComponent], 'ListBaseComponent')
    full_height: base_component_or(bool) = attribute(origin='fullHeight')
    min_width: base_component_or(float) = attribute(origin='minWidth')
    ratio: base_component_or(List[base_component_or(float)], 'ListBaseComponentOrFloat')
    vertical_align: base_component_or(VerticalAlign) = attribute(origin='verticalAlign')


class SideBySideLayoutV1(BaseLayoutV1, spec_value=ComponentType.LAYOUT_SIDE_BY_SIDE):
    controls: BaseComponent
    items: base_component_or(List[BaseComponent], 'ListBaseComponent')
    min_item_width: base_component_or(float) = attribute(origin='minItemWidth')


class SidebarLayoutV1(BaseLayoutV1, spec_value=ComponentType.LAYOUT_SIDEBAR):
    content: BaseComponent
    controls: BaseComponent
    controls_width: base_component_or(float) = attribute(origin='controlsWidth')
    extra_controls: BaseComponent = attribute(origin='extraControls')
    min_width: base_component_or(float) = attribute(origin='minWidth')
