from decimal import Decimal
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class Requester(BaseTolokaObject):
    """Contains information about the customer and the account balance

    Attributes:
        id: Requester ID.
        balance: Account balance in dollars.
        public_name: The requester's name in Toloka.
        company:
    """

    class Company(BaseTolokaObject):

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
            superintendent_id: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        id: Optional[str]
        superintendent_id: Optional[str]

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
        balance: Optional[Decimal] = ...,
        public_name: Optional[Dict[str, str]] = ...,
        company: Optional[Company] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    balance: Optional[Decimal]
    public_name: Optional[Dict[str, str]]
    company: Optional[Company]
