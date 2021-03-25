__all__ = ['Requester']
from attr.validators import optional, instance_of
from decimal import Decimal
from typing import Dict

from .primitives.base import attribute, BaseTolokaObject


class Requester(BaseTolokaObject):
    """Contains information about the customer and the account balance

    Attributes:
        id: Requester ID.
        balance: Account balance in dollars.
        public_name: The requester's name in Toloka.
        company:
    """

    class Company(BaseTolokaObject):
        id: str
        superintendent_id: str

    id: str
    balance: Decimal = attribute(validator=optional(instance_of(Decimal)))
    public_name: Dict[str, str]
    company: Company
