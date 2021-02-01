from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base import BaseComponent, BaseTemplate, VersionedBaseComponent


class BasePluginV1(VersionedBaseComponent):

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(self, *, version: Optional[str] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]

class HotkeysPluginV1(BasePluginV1):

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
        key_a: Optional[Any] = ...,
        key_b: Optional[Any] = ...,
        key_c: Optional[Any] = ...,
        key_d: Optional[Any] = ...,
        key_e: Optional[Any] = ...,
        key_f: Optional[Any] = ...,
        key_g: Optional[Any] = ...,
        key_h: Optional[Any] = ...,
        key_i: Optional[Any] = ...,
        key_j: Optional[Any] = ...,
        key_k: Optional[Any] = ...,
        key_l: Optional[Any] = ...,
        key_m: Optional[Any] = ...,
        key_n: Optional[Any] = ...,
        key_o: Optional[Any] = ...,
        key_p: Optional[Any] = ...,
        key_q: Optional[Any] = ...,
        key_r: Optional[Any] = ...,
        key_s: Optional[Any] = ...,
        key_t: Optional[Any] = ...,
        key_u: Optional[Any] = ...,
        key_v: Optional[Any] = ...,
        key_w: Optional[Any] = ...,
        key_x: Optional[Any] = ...,
        key_y: Optional[Any] = ...,
        key_z: Optional[Any] = ...,
        key_0: Optional[Any] = ...,
        key_1: Optional[Any] = ...,
        key_2: Optional[Any] = ...,
        key_3: Optional[Any] = ...,
        key_4: Optional[Any] = ...,
        key_5: Optional[Any] = ...,
        key_6: Optional[Any] = ...,
        key_7: Optional[Any] = ...,
        key_8: Optional[Any] = ...,
        key_9: Optional[Any] = ...,
        key_up: Optional[Any] = ...,
        key_down: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    key_a: Optional[Any]
    key_b: Optional[Any]
    key_c: Optional[Any]
    key_d: Optional[Any]
    key_e: Optional[Any]
    key_f: Optional[Any]
    key_g: Optional[Any]
    key_h: Optional[Any]
    key_i: Optional[Any]
    key_j: Optional[Any]
    key_k: Optional[Any]
    key_l: Optional[Any]
    key_m: Optional[Any]
    key_n: Optional[Any]
    key_o: Optional[Any]
    key_p: Optional[Any]
    key_q: Optional[Any]
    key_r: Optional[Any]
    key_s: Optional[Any]
    key_t: Optional[Any]
    key_u: Optional[Any]
    key_v: Optional[Any]
    key_w: Optional[Any]
    key_x: Optional[Any]
    key_y: Optional[Any]
    key_z: Optional[Any]
    key_0: Optional[Any]
    key_1: Optional[Any]
    key_2: Optional[Any]
    key_3: Optional[Any]
    key_4: Optional[Any]
    key_5: Optional[Any]
    key_6: Optional[Any]
    key_7: Optional[Any]
    key_8: Optional[Any]
    key_9: Optional[Any]
    key_up: Optional[Any]
    key_down: Optional[Any]

class TriggerPluginV1(BasePluginV1):

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
        action: Optional[BaseComponent] = ...,
        condition: Optional[BaseComponent] = ...,
        fire_immediately: Optional[Union[BaseComponent, bool]] = ...,
        on_change_of: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    action: Optional[BaseComponent]
    condition: Optional[BaseComponent]
    fire_immediately: Optional[Union[BaseComponent, bool]]
    on_change_of: Optional[BaseComponent]

class TolokaPluginV1(BasePluginV1):

    class TolokaPluginLayout(BaseTemplate):

        class Kind(Enum):
            ...

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
            kind: Optional[Kind] = ...,
            task_width: Optional[float] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        kind: Optional[Kind]
        task_width: Optional[float]

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
        layout: Optional[Union[BaseComponent, TolokaPluginLayout]] = ...,
        notifications: Optional[Union[BaseComponent, List[BaseComponent]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    layout: Optional[Union[BaseComponent, TolokaPluginLayout]]
    notifications: Optional[Union[BaseComponent, List[BaseComponent]]]
