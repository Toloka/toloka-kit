__all__ = ['Owner']
from .primitives.base import BaseTolokaObject


class Owner(BaseTolokaObject):
    id: str
    myself: bool
    company_id: str
