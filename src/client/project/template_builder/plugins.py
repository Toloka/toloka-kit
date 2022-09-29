__all__ = [
    'BasePluginV1',
    'ImageAnnotationHotkeysPluginV1',
    'TextAnnotationHotkeysPluginV1',
    'HotkeysPluginV1',
    'TriggerPluginV1',
    'TolokaPluginV1',
]

from enum import unique
from typing import List, Any


from .base import VersionedBaseComponentMetaclass, BaseComponent, ComponentType, BaseTemplate, base_component_or
from ....util._codegen import attribute, expand
from ....util._extendable_enum import ExtendableStrEnum


class BasePluginV1(BaseComponent, metaclass=VersionedBaseComponentMetaclass):
    """Plugins that provide expanded functionality. For example, you can use plugin.hotkeys to set up shortcuts.

    """

    pass


class ImageAnnotationHotkeysPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_IMAGE_ANNOTATION_HOTKEYS):
    """Used to set hotkeys for the field.image-annotation component.

    You can set hotkeys to select area types and selection modes and to confirm or cancel area creation. When setting
    hotkeys, you can use the up and down arrows (up,down), numbers, and Latin letters.

    Attributes:
        cancel: Keyboard shortcut for canceling area creation.
        confirm: Keyboard shortcut for confirming area creation.
        labels: Keyboard shortcuts for choosing area types. They're assigned to buttons in the order they are shown if
            you enabled the option to choose multiple area types.
        modes: Keyboard shortcuts for choosing selection modes.
    """

    class Mode(BaseTemplate):
        """
        Mode

        Attributes:
            point: Keyboard shortcut for selecting areas using points.
            polygon: Keyboard shortcut for selecting areas using polygons.
            rectangle: Keyboard shortcut for selecting areas using rectangles.
            select: Keyboard shortcut for selecting shapes and points.
        """

        point: str = attribute(kw_only=True)
        polygon: str = attribute(kw_only=True)
        rectangle: str = attribute(kw_only=True)
        select: str = attribute(kw_only=True)

    cancel: base_component_or(str) = attribute(kw_only=True)
    confirm: base_component_or(str) = attribute(kw_only=True)
    labels: base_component_or(List[str], 'ListStr') = attribute(kw_only=True)  # noqa: F821
    modes: base_component_or(Mode) = attribute(kw_only=True)

ImageAnnotationHotkeysPluginV1.__init__ = \
    expand('modes', ImageAnnotationHotkeysPluginV1.Mode)(ImageAnnotationHotkeysPluginV1.__init__)


class TextAnnotationHotkeysPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_TEXT_ANNOTATION_HOTKEYS):
    """Use this to set keyboard shortcuts for the field.text-annotation component.

    Attributes:
        labels: Keyboard shortcuts for selecting categories. They're assigned to buttons with categories in the order
            they're shown.
        remove: Use this property to allow a Toloker to deselect an entire line or part of it. The key that you
            assign to this property will deselect.
    """

    labels: base_component_or(List[str], 'ListStr')  # noqa: F821
    remove: base_component_or(str)


class HotkeysPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_HOTKEYS):
    """Lets you set keyboard shortcuts for actions.

    Attributes:
        key_ + [a-z|0-9|up|down]: An action that is triggered when you press the specified keyboard key. The keyboard
            shortcut is set in the key, and the action is specified in the value

    Example:
        How to create hotkeys for classification buttons.

        >>> hot_keys_plugin = tb.HotkeysPluginV1(
        >>>     key_1=tb.SetActionV1(tb.OutputData('result'), 'cat'),
        >>>     key_2=tb.SetActionV1(tb.OutputData('result'), 'dog'),
        >>>     key_3=tb.SetActionV1(tb.OutputData('result'), 'other'),
        >>> )
        ...
    """

    key_a: base_component_or(Any) = attribute(default=None, origin='a', kw_only=True)
    key_b: base_component_or(Any) = attribute(default=None, origin='b', kw_only=True)
    key_c: base_component_or(Any) = attribute(default=None, origin='c', kw_only=True)
    key_d: base_component_or(Any) = attribute(default=None, origin='d', kw_only=True)
    key_e: base_component_or(Any) = attribute(default=None, origin='e', kw_only=True)
    key_f: base_component_or(Any) = attribute(default=None, origin='f', kw_only=True)
    key_g: base_component_or(Any) = attribute(default=None, origin='g', kw_only=True)
    key_h: base_component_or(Any) = attribute(default=None, origin='h', kw_only=True)
    key_i: base_component_or(Any) = attribute(default=None, origin='i', kw_only=True)
    key_j: base_component_or(Any) = attribute(default=None, origin='j', kw_only=True)
    key_k: base_component_or(Any) = attribute(default=None, origin='k', kw_only=True)
    key_l: base_component_or(Any) = attribute(default=None, origin='l', kw_only=True)
    key_m: base_component_or(Any) = attribute(default=None, origin='m', kw_only=True)
    key_n: base_component_or(Any) = attribute(default=None, origin='n', kw_only=True)
    key_o: base_component_or(Any) = attribute(default=None, origin='o', kw_only=True)
    key_p: base_component_or(Any) = attribute(default=None, origin='p', kw_only=True)
    key_q: base_component_or(Any) = attribute(default=None, origin='q', kw_only=True)
    key_r: base_component_or(Any) = attribute(default=None, origin='r', kw_only=True)
    key_s: base_component_or(Any) = attribute(default=None, origin='s', kw_only=True)
    key_t: base_component_or(Any) = attribute(default=None, origin='t', kw_only=True)
    key_u: base_component_or(Any) = attribute(default=None, origin='u', kw_only=True)
    key_v: base_component_or(Any) = attribute(default=None, origin='v', kw_only=True)
    key_w: base_component_or(Any) = attribute(default=None, origin='w', kw_only=True)
    key_x: base_component_or(Any) = attribute(default=None, origin='x', kw_only=True)
    key_y: base_component_or(Any) = attribute(default=None, origin='y', kw_only=True)
    key_z: base_component_or(Any) = attribute(default=None, origin='z', kw_only=True)
    key_0: base_component_or(Any) = attribute(default=None, origin='0', kw_only=True)
    key_1: base_component_or(Any) = attribute(default=None, origin='1', kw_only=True)
    key_2: base_component_or(Any) = attribute(default=None, origin='2', kw_only=True)
    key_3: base_component_or(Any) = attribute(default=None, origin='3', kw_only=True)
    key_4: base_component_or(Any) = attribute(default=None, origin='4', kw_only=True)
    key_5: base_component_or(Any) = attribute(default=None, origin='5', kw_only=True)
    key_6: base_component_or(Any) = attribute(default=None, origin='6', kw_only=True)
    key_7: base_component_or(Any) = attribute(default=None, origin='7', kw_only=True)
    key_8: base_component_or(Any) = attribute(default=None, origin='8', kw_only=True)
    key_9: base_component_or(Any) = attribute(default=None, origin='9', kw_only=True)
    key_up: base_component_or(Any) = attribute(default=None, origin='up', kw_only=True)
    key_down: base_component_or(Any) = attribute(default=None, origin='down', kw_only=True)


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
        How to save Toloker's coordinates to the output.

        >>> coordinates_save_plugin = tb.plugins.TriggerPluginV1(
        >>>     fire_immediately=True,
        >>>     action=tb.actions.SetActionV1(
        >>>         data=tb.data.OutputData(path='performer_coordinates'),
        >>>         payload=tb.data.LocationData()
        >>>     ),
        >>> )
        ...
    """

    action: BaseComponent = attribute(kw_only=True)
    condition: BaseComponent = attribute(kw_only=True)
    fire_immediately: base_component_or(bool) = attribute(origin='fireImmediately', kw_only=True)
    on_change_of: BaseComponent = attribute(origin='onChangeOf', kw_only=True)


class TolokaPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_TOLOKA):
    """A plugin with extra settings for tasks in Toloka.

    Attributes:
        layout: Settings for the task appearance in Toloka.
        notifications: Notifications shown at the top of the page.

    Example:
        How to set the task width on the task page.

        >>> task_width_plugin = tb.plugins.TolokaPluginV1(
        >>>     'scroll',
        >>>     task_width=400,
        >>> )
        ...
    """

    class TolokaPluginLayout(BaseTemplate):
        """How to display task.

        """

        @unique
        class Kind(ExtendableStrEnum):
            """An enumeration.

            Attributes:
                SCROLL: (default) display multiple tasks on the page at the same time.
                PAGER: display only one task on the page, with a button to switch between tasks at the bottom.
            """

            PAGER = 'pager'
            SCROLL = 'scroll'

        kind: Kind
        task_width: base_component_or(float) = attribute(origin='taskWidth', kw_only=True)

    layout: base_component_or(TolokaPluginLayout) = attribute(factory=TolokaPluginLayout)
    notifications: base_component_or(List[BaseComponent], 'ListBaseComponent') = attribute(kw_only=True)  # noqa: F821

TolokaPluginV1.__init__ = expand('layout', TolokaPluginV1.TolokaPluginLayout)(TolokaPluginV1.__init__)
