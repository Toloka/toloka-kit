from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base import BaseComponent, VersionedBaseComponent


class BaseLayoutV1(VersionedBaseComponent):
    """Options for positioning elements in the interface, such as in columns or side-by-side.

    If you have more than one element in the interface, these components will help you arrange them the way you want.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        validation: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    validation: Optional[BaseComponent]

class BarsLayoutV1(BaseLayoutV1):
    """A component that adds top and bottom bars to the content.

    You can use other components inside each part of this component, such as images, text, or options.

    The top bar is located at the top edge of the component, and the bottom one is at the bottom edge. The content is
    placed between the bars and takes up all available space.
    Attributes:
        bar_after: The bar displayed at the bottom edge of the component.
        bar_before: The bar displayed at the top edge of the component.
        content: The main content.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        validation: Optional[BaseComponent] = ...,
        content: Optional[BaseComponent] = ...,
        bar_after: Optional[BaseComponent] = ...,
        bar_before: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    validation: Optional[BaseComponent]
    content: Optional[BaseComponent]
    bar_after: Optional[BaseComponent]
    bar_before: Optional[BaseComponent]

class ColumnsLayoutV1(BaseLayoutV1):
    """A component for placing content in columns.

    Use it to customize the display of content: set the column width and adjust the vertical alignment of content.
    Attributes:
        full_height: Switches the component to column mode at full height and with individual scrolling. Otherwise, the
            height is determined by the height of the column that is filled in the most.
        items: Columns to divide the interface into.
        min_width: The minimum width of the component; if it is narrower, columns are output sequentially, one by one.
        ratio: An array of values that specify the relative width of columns. For example, if you have 3 columns, the
            value [1,2,1] divides the space into 4 parts and the column in the middle is twice as large as the other
            columns.
            If the number of columns exceeds the number of values in the ratio property, the values are repeated. For
            example, if you have 4 columns and the ratio is set to [1,2], the result is the same as for [1,2,1,2].
            If the number of columns is less than the number of values in the ratio property, extra values are simply
            ignored.
        validation: Validation based on condition.
        vertical_align: Vertical alignment of column content.
    """

    class VerticalAlign(Enum):
        """Vertical alignment of column content.

        top — Aligned to the top of a column.
        middle — Aligned to the middle of the column that is filled in the most.
        bottom — Aligned to the bottom of a column.
        """
        ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        validation: Optional[BaseComponent] = ...,
        items: Optional[Union[BaseComponent, List[BaseComponent]]] = ...,
        full_height: Optional[Union[BaseComponent, bool]] = ...,
        min_width: Optional[Union[BaseComponent, float]] = ...,
        ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = ...,
        vertical_align: Optional[Union[BaseComponent, VerticalAlign]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    validation: Optional[BaseComponent]
    items: Optional[Union[BaseComponent, List[BaseComponent]]]
    full_height: Optional[Union[BaseComponent, bool]]
    min_width: Optional[Union[BaseComponent, float]]
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]]
    vertical_align: Optional[Union[BaseComponent, VerticalAlign]]

class SideBySideLayoutV1(BaseLayoutV1):
    """The component displays several data blocks of the same width on a single horizontal panel.

    For example, you can use this to compare several photos.

    You can set the minimum width for data blocks.
    Attributes:
        controls: Components that let users perform the required actions.
            For example: field.checkbox-group or field.button-radio-group.
        items: An array of data blocks.
        min_item_width: The minimum width of a data block, at least 400 pixels.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        validation: Optional[BaseComponent] = ...,
        controls: Optional[BaseComponent] = ...,
        items: Optional[Union[BaseComponent, List[BaseComponent]]] = ...,
        min_item_width: Optional[Union[BaseComponent, float]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    validation: Optional[BaseComponent]
    controls: Optional[BaseComponent]
    items: Optional[Union[BaseComponent, List[BaseComponent]]]
    min_item_width: Optional[Union[BaseComponent, float]]

class SidebarLayoutV1(BaseLayoutV1):
    """An option for placing (layout) items, which lets you arrange on a page:

    * The main content block.
    * An adjacent panel with controls.

    The minWidth property sets the threshold for switching between widescreen and compact modes: when the width of the
    layout.sidebar component itself becomes less than the value set by the minWidth property, compact mode is enabled.

    In widescreen mode, the control panel is located to the right of the main block.

    In compact mode, controls stretch to the entire width and are located under each other.

    To add an extra panel with controls, use the extraControls property.
    Attributes:
        content: Content placed in the main area.
        controls: Content of the control panel.
        controls_width: The width of the control panel in widescreen mode. In compact mode, the panel takes up the
            entire available width. Default: 200 pixels.
        extra_controls: An additional panel with controls. Located below the main panel.
        min_width: The minimum width, in pixels, for widescreen mode. If the component width becomes less than the
            specified value, the interface switches to compact mode. Default: 400 pixels.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        validation: Optional[BaseComponent] = ...,
        content: Optional[BaseComponent] = ...,
        controls: Optional[BaseComponent] = ...,
        controls_width: Optional[Union[BaseComponent, float]] = ...,
        extra_controls: Optional[BaseComponent] = ...,
        min_width: Optional[Union[BaseComponent, float]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    validation: Optional[BaseComponent]
    content: Optional[BaseComponent]
    controls: Optional[BaseComponent]
    controls_width: Optional[Union[BaseComponent, float]]
    extra_controls: Optional[BaseComponent]
    min_width: Optional[Union[BaseComponent, float]]
