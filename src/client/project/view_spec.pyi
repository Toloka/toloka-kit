from enum import Enum
from typing import Any, Dict, List, Optional

from ..primitives.base import BaseTolokaObject
from .template_builder import TemplateBuilder


class ViewSpec(BaseTolokaObject):

    class Type(Enum):
        ...

    class Settings(BaseTolokaObject):
        """ViewSpec Settings

        Attributes:
            show_finish: Show the Back to main page button.
            show_fullscreen: Show the Expand to fullscreen button.
            show_instructions: Show the Instructions button.
            show_message: Show the Message for the requester button.
            show_reward: Show the price per task page.
            show_skip: Show the Skip button.
            show_submit: Show the Next button.
            show_timer: Show the timer.
            show_title: Show the project name in task titles.
        """

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
            show_finish: Optional[bool] = ...,
            show_fullscreen: Optional[bool] = ...,
            show_instructions: Optional[bool] = ...,
            show_message: Optional[bool] = ...,
            show_reward: Optional[bool] = ...,
            show_skip: Optional[bool] = ...,
            show_submit: Optional[bool] = ...,
            show_timer: Optional[bool] = ...,
            show_title: Optional[bool] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        show_finish: Optional[bool]
        show_fullscreen: Optional[bool]
        show_instructions: Optional[bool]
        show_message: Optional[bool]
        show_reward: Optional[bool]
        show_skip: Optional[bool]
        show_submit: Optional[bool]
        show_timer: Optional[bool]
        show_title: Optional[bool]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, *, settings: Optional[Settings] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    settings: Optional[Settings]

class ClassicViewSpec(ViewSpec):

    class Assets(BaseTolokaObject):

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
            script_urls: Optional[List[str]] = ...,
            style_urls: Optional[List[str]] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        script_urls: Optional[List[str]]
        style_urls: Optional[List[str]]

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
        settings: Optional[ViewSpec.Settings] = ...,
        script: Optional[str] = ...,
        markup: Optional[str] = ...,
        styles: Optional[str] = ...,
        assets: Optional[Assets] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    settings: Optional[ViewSpec.Settings]
    script: Optional[str]
    markup: Optional[str]
    styles: Optional[str]
    assets: Optional[Assets]

class TemplateBuilderViewSpec(ViewSpec):

    def unstructure(self): ...

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
        settings: Optional[ViewSpec.Settings] = ...,
        config: Optional[TemplateBuilder] = ...,
        core_version: Optional[str] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    settings: Optional[ViewSpec.Settings]
    config: Optional[TemplateBuilder]
    core_version: Optional[str]
