__all__ = [
    'BasePluginV1',
    'HotkeysPluginV1',
    'TriggerPluginV1',
    'TolokaPluginV1'
]
from enum import Enum, unique
from typing import List, Any

from ...primitives.base import attribute

from .base import VersionedBaseComponent, BaseComponent, ComponentType, BaseTemplate, base_component_or


class BasePluginV1(VersionedBaseComponent):
    """Plugins that provide expanded functionality. For example, you can use plugin.hotkeys to set up shortcuts.

    """

    pass


class HotkeysPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_HOTKEYS):
    """Lets you set keyboard shortcuts for actions.

    Attributes:
        key_ + [a-z|0-9|up|down]: An action that is triggered when you press the specified keyboard key. The keyboard
            shortcut is set in the key, and the action is specified in the value
    """

    key_a: base_component_or(Any) = attribute(default=None, origin='a')
    key_b: base_component_or(Any) = attribute(default=None, origin='b')
    key_c: base_component_or(Any) = attribute(default=None, origin='c')
    key_d: base_component_or(Any) = attribute(default=None, origin='d')
    key_e: base_component_or(Any) = attribute(default=None, origin='e')
    key_f: base_component_or(Any) = attribute(default=None, origin='f')
    key_g: base_component_or(Any) = attribute(default=None, origin='g')
    key_h: base_component_or(Any) = attribute(default=None, origin='h')
    key_i: base_component_or(Any) = attribute(default=None, origin='i')
    key_j: base_component_or(Any) = attribute(default=None, origin='j')
    key_k: base_component_or(Any) = attribute(default=None, origin='k')
    key_l: base_component_or(Any) = attribute(default=None, origin='l')
    key_m: base_component_or(Any) = attribute(default=None, origin='m')
    key_n: base_component_or(Any) = attribute(default=None, origin='n')
    key_o: base_component_or(Any) = attribute(default=None, origin='o')
    key_p: base_component_or(Any) = attribute(default=None, origin='p')
    key_q: base_component_or(Any) = attribute(default=None, origin='q')
    key_r: base_component_or(Any) = attribute(default=None, origin='r')
    key_s: base_component_or(Any) = attribute(default=None, origin='s')
    key_t: base_component_or(Any) = attribute(default=None, origin='t')
    key_u: base_component_or(Any) = attribute(default=None, origin='u')
    key_v: base_component_or(Any) = attribute(default=None, origin='v')
    key_w: base_component_or(Any) = attribute(default=None, origin='w')
    key_x: base_component_or(Any) = attribute(default=None, origin='x')
    key_y: base_component_or(Any) = attribute(default=None, origin='y')
    key_z: base_component_or(Any) = attribute(default=None, origin='z')
    key_0: base_component_or(Any) = attribute(default=None, origin='0')
    key_1: base_component_or(Any) = attribute(default=None, origin='1')
    key_2: base_component_or(Any) = attribute(default=None, origin='2')
    key_3: base_component_or(Any) = attribute(default=None, origin='3')
    key_4: base_component_or(Any) = attribute(default=None, origin='4')
    key_5: base_component_or(Any) = attribute(default=None, origin='5')
    key_6: base_component_or(Any) = attribute(default=None, origin='6')
    key_7: base_component_or(Any) = attribute(default=None, origin='7')
    key_8: base_component_or(Any) = attribute(default=None, origin='8')
    key_9: base_component_or(Any) = attribute(default=None, origin='9')
    key_up: base_component_or(Any) = attribute(default=None, origin='up')
    key_down: base_component_or(Any) = attribute(default=None, origin='down')


class TriggerPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_TRIGGER):
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

    Example:
        How to save the performer coordinates to the output.

        >>> coordinates_save_plugin = tb.plugins.TriggerPluginV1(
        >>>     fire_immediately=True,
        >>>     action=tb.actions.SetActionV1(
        >>>         data=tb.data.OutputData(path='performer_coordinates'),
        >>>         payload=tb.data.LocationData()
        >>>     ),
        >>> )
        ...
    """

    action: BaseComponent
    condition: BaseComponent
    fire_immediately: base_component_or(bool) = attribute(origin='fireImmediately')
    on_change_of: BaseComponent = attribute(origin='onChangeOf')


class TolokaPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_TOLOKA):
    """A plugin with extra settings for tasks in Toloka.

    Attributes:
        layout: Settings for the task appearance in Toloka.
        notifications: Notifications shown at the top of the page.

    Example:
        How to set the task width on the task page.

        >>> task_width_plugin = tb.plugins.TolokaPluginV1(
        >>>     layout = tb.plugins.TolokaPluginV1.TolokaPluginLayout(
        >>>         kind='scroll',
        >>>         task_width=400,
        >>>     )
        >>> )
        ...
    """

    class TolokaPluginLayout(BaseTemplate):
        """How to display task.

        """

        @unique
        class Kind(Enum):
            """scroll (default) — display multiple tasks on the page at the same time.

            pager — display only one task on the page, with a button to switch between tasks at the bottom.
            """

            PAGER = 'pager'
            SCROLL = 'scroll'

        kind: Kind = Kind.SCROLL
        task_width: float = attribute(origin='taskWidth')

    layout: base_component_or(TolokaPluginLayout) = attribute(factory=TolokaPluginLayout)
    notifications: base_component_or(List[BaseComponent], 'ListBaseComponent')
