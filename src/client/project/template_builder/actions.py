__all__ = [
    'BaseActionV1',
    'BulkActionV1',
    'NotifyActionV1',
    'OpenCloseActionV1',
    'OpenLinkActionV1',
    'PlayPauseActionV1',
    'RotateActionV1',
    'SetActionV1',
    'ToggleActionV1',
]
from enum import unique
from typing import List, Any

from .base import (
    BaseTemplate,
    ComponentType,
    RefComponent,
    BaseComponent,
    VersionedBaseComponentMetaclass,
    base_component_or
)
from ....util._codegen import attribute
from ....util._extendable_enum import ExtendableStrEnum


class BaseActionV1(BaseComponent, metaclass=VersionedBaseComponentMetaclass):
    """Perform various actions, such as showing notifications.

    """

    pass


class BulkActionV1(BaseActionV1, spec_value=ComponentType.ACTION_BULK):
    """Use this component to call multiple actions at the same time, like to show more than one notification when a button is clicked.

    Actions are invoked in the order in which they are listed. This means that if two actions write a value to the same
    variable, the variable will always have the second value.
    Attributes:
        payload: An array of actions that you want to call.
    """

    payload: base_component_or(List[BaseComponent], 'ListBaseComponent')  # noqa: F821


class NotifyActionV1(BaseActionV1, spec_value=ComponentType.ACTION_NOTIFY):
    """The component creates a message in the lower-left corner of the screen.

    You can set the how long the message will be active, the delay before displaying it, and the background color.
    Attributes:
        payload: Parameters for the message.
    """

    class Payload(BaseTemplate):
        """Parameters for the message.

        Attributes:
            content: Message text
            theme: The background color of the message.
            delay: The duration of the delay (in milliseconds) before the message appears.
            duration: The duration of the message activity (in milliseconds), which includes the duration of the delay
                before displaying it.
                For example, if duration is 1000 and delay is 400, the message will be displayed for
                600 milliseconds.
        """

        @unique
        class Theme(ExtendableStrEnum):
            """The background color of the message.

            Attributes:
                INFO: blue
                SUCCESS: green
                WARNING: yellow
                DANGER: red
            """

            DANGER = 'danger'
            INFO = 'info'
            SUCCESS = 'success'
            WARNING = 'warning'

        content: base_component_or(Any)
        theme: base_component_or(Theme)
        delay: base_component_or(float) = attribute(kw_only=True)
        duration: base_component_or(float) = attribute(kw_only=True)

    payload: base_component_or(Payload)


class OpenCloseActionV1(BaseActionV1, spec_value=ComponentType.ACTION_OPEN_CLOSE):
    """This component changes the display mode of another component by opening or closing it.

    What happens to the component depends on the type of component:
        view.image — expands the image to full screen.
        view.collapse — expands or collapses a collapsible section of content.
    Attributes:
        view: Points to the component to perform the action with.
    """

    view: base_component_or(RefComponent)


class OpenLinkActionV1(BaseActionV1, spec_value=ComponentType.ACTION_OPEN_LINK):
    """Opens a new tab in the browser with the specified web page.

    For example, you can open a link when a button is clicked.
    Attributes:
        payload: URL of the web page.
    """

    payload: base_component_or(Any)


class PlayPauseActionV1(BaseActionV1, spec_value=ComponentType.ACTION_PLAY_PAUSE):
    """This component controls audio or video playback. It stops playback in progress or starts if it is stopped.

    For example, this component will allow you to play two videos simultaneously.

    You can also stop or start playback for some event (plugin. trigger) or by pressing the hotkey (plugin.hotkeys).
    Attributes:
        view: Points to the component that plays audio or video.
    """

    view: base_component_or(RefComponent)


class RotateActionV1(BaseActionV1, spec_value=ComponentType.ACTION_ROTATE):
    """Rotates the specified component by 90 degrees.

    By default it rotates to the right, but you can specify the direction in the payload property.
    Attributes:
        view: Points to the component to perform the action with.
        payload: Sets the direction of rotation.
    """

    @unique
    class Payload(ExtendableStrEnum):
        LEFT = 'left'
        RIGHT = 'right'

    view: base_component_or(RefComponent)
    payload: base_component_or(Payload)


class SetActionV1(BaseActionV1, spec_value=ComponentType.ACTION_SET):
    """Sets the value from payload in the data in the data property.

    Attributes:
        data: Data with values that will be processed or changed.
        payload: The value to write to the data.
    """

    data: BaseComponent
    payload: base_component_or(Any)


class ToggleActionV1(BaseActionV1, spec_value=ComponentType.ACTION_TOGGLE):
    """The component changes the value in the data from true to false and vice versa.

    Attributes:
        data: Data in which the value will be changed. The data type must be boolean.
    """

    data: BaseComponent
