from attr.validators import optional, instance_of
from decimal import Decimal
from typing import Dict

from .primitives.base import attribute, BaseTolokaObject


class Requester(BaseTolokaObject):

    class Company(BaseTolokaObject):
        id: str
        superintendent_id: str

    id: str
    balance: Decimal = attribute(validator=optional(instance_of(Decimal)))
    public_name: Dict[str, str]
    company: Company
