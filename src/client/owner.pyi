from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class Owner(BaseTolokaObject):
    """Parameters of the customer who created an object.

    Attributes:
        id: Customer ID.
        myself: An object accessory marker.
            Possible values:
                * True - an object created by the customer whose OAuth-токен in the request;
                * False - an object does not belong to the customer whose OAuth-токен in the request.
        company_id: ID of the customer's company.
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
        id: Optional[str] = ...,
        myself: Optional[bool] = ...,
        company_id: Optional[str] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    myself: Optional[bool]
    company_id: Optional[str]
