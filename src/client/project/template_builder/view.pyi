from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base import (
    BaseComponent,
    BaseTemplate,
    ListDirection,
    ListSize,
    VersionedBaseComponent
)


class BaseViewV1(VersionedBaseComponent):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]

class ActionButtonViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        action: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    action: Optional[BaseComponent]

class AlertViewV1(BaseViewV1):

    class Theme(Enum):
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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        content: Optional[BaseComponent] = ...,
        theme: Optional[Union[BaseComponent, Theme]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    content: Optional[BaseComponent]
    theme: Optional[Union[BaseComponent, Theme]]

class AudioViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        url: Optional[Any] = ...,
        loop: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    url: Optional[Any]
    loop: Optional[Union[BaseComponent, bool]]

class CollapseViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        content: Optional[BaseComponent] = ...,
        label: Optional[Any] = ...,
        default_opened: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    validation: Optional[BaseComponent]
    content: Optional[BaseComponent]
    label: Optional[Any]
    default_opened: Optional[Union[BaseComponent, bool]]

class DeviceFrameViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        content: Optional[BaseComponent] = ...,
        full_height: Optional[Union[BaseComponent, bool]] = ...,
        max_width: Optional[Union[BaseComponent, float]] = ...,
        min_width: Optional[Union[BaseComponent, float]] = ...,
        ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    content: Optional[BaseComponent]
    full_height: Optional[Union[BaseComponent, bool]]
    max_width: Optional[Union[BaseComponent, float]]
    min_width: Optional[Union[BaseComponent, float]]
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]]

class DividerViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]

class GroupViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        content: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    content: Optional[BaseComponent]

class IframeViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        url: Optional[Union[BaseComponent, str]] = ...,
        full_height: Optional[Union[BaseComponent, bool]] = ...,
        max_width: Optional[Union[BaseComponent, float]] = ...,
        min_width: Optional[Union[BaseComponent, float]] = ...,
        ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    url: Optional[Union[BaseComponent, str]]
    full_height: Optional[Union[BaseComponent, bool]]
    max_width: Optional[Union[BaseComponent, float]]
    min_width: Optional[Union[BaseComponent, float]]
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]]

class ImageViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        url: Optional[Any] = ...,
        full_height: Optional[Union[BaseComponent, bool]] = ...,
        max_width: Optional[Union[BaseComponent, float]] = ...,
        min_width: Optional[Union[BaseComponent, float]] = ...,
        no_border: Optional[Union[BaseComponent, bool]] = ...,
        no_lazy_load: Optional[Union[BaseComponent, bool]] = ...,
        popup: Optional[Union[BaseComponent, bool]] = ...,
        ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = ...,
        rotatable: Optional[Union[BaseComponent, bool]] = ...,
        scrollable: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    url: Optional[Any]
    full_height: Optional[Union[BaseComponent, bool]]
    max_width: Optional[Union[BaseComponent, float]]
    min_width: Optional[Union[BaseComponent, float]]
    no_border: Optional[Union[BaseComponent, bool]]
    no_lazy_load: Optional[Union[BaseComponent, bool]]
    popup: Optional[Union[BaseComponent, bool]]
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]]
    rotatable: Optional[Union[BaseComponent, bool]]
    scrollable: Optional[Union[BaseComponent, bool]]

class LabeledListViewV1(BaseViewV1):

    class Item(BaseTemplate):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(
            self,*,
            content: Optional[BaseComponent] = ...,
            label: Optional[Any] = ...,
            center_label: Optional[Union[BaseComponent, bool]] = ...,
            hint: Optional[Any] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        content: Optional[BaseComponent]
        label: Optional[Any]
        center_label: Optional[Union[BaseComponent, bool]]
        hint: Optional[Any]

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        items: Optional[Union[BaseComponent, List[Union[BaseComponent, Item]]]] = ...,
        min_width: Optional[Union[BaseComponent, float]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    items: Optional[Union[BaseComponent, List[Union[BaseComponent, Item]]]]
    min_width: Optional[Union[BaseComponent, float]]

class LinkViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        url: Optional[Any] = ...,
        content: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    url: Optional[Any]
    content: Optional[Any]

class ListViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        items: Optional[Union[BaseComponent, List[BaseComponent]]] = ...,
        direction: Optional[Union[BaseComponent, ListDirection]] = ...,
        size: Optional[Union[BaseComponent, ListSize]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    items: Optional[Union[BaseComponent, List[BaseComponent]]]
    direction: Optional[Union[BaseComponent, ListDirection]]
    size: Optional[Union[BaseComponent, ListSize]]

class MarkdownViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        content: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    content: Optional[Any]

class TextViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        content: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    content: Optional[Any]

class VideoViewV1(BaseViewV1):

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
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        full_height: Optional[Union[BaseComponent, bool]] = ...,
        max_width: Optional[Union[BaseComponent, float]] = ...,
        min_width: Optional[Union[BaseComponent, float]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    full_height: Optional[Union[BaseComponent, bool]]
    max_width: Optional[Union[BaseComponent, float]]
    min_width: Optional[Union[BaseComponent, float]]
