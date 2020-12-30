from typing import Dict

from .primitives.base import BaseTolokaObject


class Requester(BaseTolokaObject):

    class Company(BaseTolokaObject):
        id: str
        superintendent_id: str

    id: str
    balance: float
    public_name: Dict[str, str]
    company: Company
