from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base import BaseComponent, VersionedBaseComponent


class BaseLayoutV1(VersionedBaseComponent):

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

    class VerticalAlign(Enum):
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
