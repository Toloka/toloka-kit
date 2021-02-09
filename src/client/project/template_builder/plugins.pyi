from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base import BaseComponent, BaseTemplate, VersionedBaseComponent


class BasePluginV1(VersionedBaseComponent):
    """Plugins that provide expanded functionality. For example, you can use plugin.hotkeys to set up shortcuts.

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

    def __init__(self, *, version: Optional[str] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]

class HotkeysPluginV1(BasePluginV1):
    """Lets you set keyboard shortcuts for actions.

    Attributes:
        key_ + [a-z|0-9|up|down]: An action that is triggered when you press the specified keyboard key. The keyboard
            shortcut is set in the key, and the action is specified in the value
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
    """Use this to configure triggers that trigger a specific action when an event occurs.

    The action is set in the action property, and the event is described in the other fields.

    The event can be triggered immediately when the task is loaded ("fireImmediately": true) or when data changes in
    the property specified in onChangeOf.

    You can also set conditions in the conditions property that must be met in order for the trigger to fire.
    Attributes:
        action: The action to perform when the trigger fires.
        condition: The condition that must be met in order to fire the trigger.
        fire_immediately: Flag indicating whether the trigger should be fired immediately after the task is loaded.
        on_change_of: The data that triggers the action when changed.
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
    """A plugin with extra settings for tasks in Toloka.

    Attributes:
        layout: Settings for the task appearance in Toloka.
        notifications: Notifications shown at the top of the page.
    """

    class TolokaPluginLayout(BaseTemplate):
        """How to display task.

        """

        class Kind(Enum):
            """scroll (default) — display multiple tasks on the page at the same time.

            pager — display only one task on the page, with a button to switch between tasks at the bottom.
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
