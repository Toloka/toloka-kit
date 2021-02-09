from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base import (
    BaseComponent,
    BaseTemplate,
    RefComponent,
    VersionedBaseComponent
)


class BaseActionV1(VersionedBaseComponent):
    """Perform various actions, such as showing notifications.

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

class BulkActionV1(BaseActionV1):
    """Use this component to call multiple actions at the same time, like to show more than one notification when a button is clicked.

    Actions are invoked in the order in which they are listed. This means that if two actions write a value to the same
    variable, the variable will always have the second value.
    Attributes:
        payload: An array of actions that you want to call.
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
        payload: Optional[Union[BaseComponent, List[BaseComponent]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    payload: Optional[Union[BaseComponent, List[BaseComponent]]]

class NotifyActionV1(BaseActionV1):
    """The component creates a message in the lower-left corner of the screen.

    You can set the how long the message will be active, the delay before displaying it, and the background color.
    Attributes:
        payload: Parameters for the message.
    """

    class Payload(BaseTemplate):
        """Parameters for the message.

        Attributes:
            content: Message text
            delay: The duration of the delay (in milliseconds) before the message appears.
            duration: The duration of the message activity (in milliseconds), which includes the duration of the delay
                before displaying it.
                For example, if duration is 1000 and delay is 400, the message will be displayed for
                600 milliseconds.
            theme: The background color of the message.
        """

        class Theme(Enum):
            """The background color of the message.

            info — blue
            success — green
            warning — yellow
            danger — red
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
            content: Optional[Any] = ...,
            theme: Optional[Union[BaseComponent, Theme]] = ...,
            delay: Optional[Union[BaseComponent, float]] = ...,
            duration: Optional[Union[BaseComponent, float]] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        content: Optional[Any]
        theme: Optional[Union[BaseComponent, Theme]]
        delay: Optional[Union[BaseComponent, float]]
        duration: Optional[Union[BaseComponent, float]]

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
        payload: Optional[Union[BaseComponent, Payload]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    payload: Optional[Union[BaseComponent, Payload]]

class OpenCloseActionV1(BaseActionV1):
    """This component changes the display mode of another component by opening or closing it.

    What happens to the component depends on the type of component:
        view.image — expands the image to full screen.
        view.collapse — expands or collapses a collapsible section of content.
    Attributes:
        view: Points to the component to perform the action with.
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
        view: Optional[Union[BaseComponent, RefComponent]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    view: Optional[Union[BaseComponent, RefComponent]]

class OpenLinkActionV1(BaseActionV1):
    """Opens a new tab in the browser with the specified web page.

    For example, you can open a link when a button is clicked.
    Attributes:
        payload: URL of the web page.
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
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    payload: Optional[Any]

class PlayPauseActionV1(BaseActionV1):
    """This component controls audio or video playback. It stops playback in progress or starts if it is stopped.

    For example, this component will allow you to play two videos simultaneously.

    You can also stop or start playback for some event (plugin. trigger) or by pressing the hotkey (plugin.hotkeys).
    Attributes:
        view: Points to the component that plays audio or video.
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
        view: Optional[Union[BaseComponent, RefComponent]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    view: Optional[Union[BaseComponent, RefComponent]]

class RotateActionV1(BaseActionV1):
    """Rotates the specified component by 90 degrees.

    By default it rotates to the right, but you can specify the direction in the payload property.
    Attributes:
        payload: Sets the direction of rotation.
        view: Points to the component to perform the action with.
    """

    class Payload(Enum):
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
        payload: Optional[Union[BaseComponent, Payload]] = ...,
        view: Optional[Union[BaseComponent, RefComponent]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    payload: Optional[Union[BaseComponent, Payload]]
    view: Optional[Union[BaseComponent, RefComponent]]

class SetActionV1(BaseActionV1):
    """Sets the value from payload in the data in the data property.

    Attributes:
        data: Data with values that will be processed or changed.
        payload: The value to write to the data.
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
        data: Optional[BaseComponent] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    payload: Optional[Any]

class ToggleActionV1(BaseActionV1):
    """The component changes the value in the data from true to false and vice versa.

    Attributes:
        data: Data in which the value will be changed. The data type must be boolean.
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
        data: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
