from typing import Any, Dict, List, Optional

from ...primitives.base import BaseTolokaObject
from .base import BaseComponent


class TemplateBuilder(BaseTolokaObject):

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
        view: Optional[BaseComponent] = ...,
        plugins: Optional[List[BaseComponent]] = ...,
        vars: Optional[Dict[str, Any]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    view: Optional[BaseComponent]
    plugins: Optional[List[BaseComponent]]
    vars: Optional[Dict[str, Any]]
