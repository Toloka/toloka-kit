__all__ = ['Parameters']
from .base import BaseTolokaObject


class Parameters(BaseTolokaObject, kw_only=False):

    def unstructure(self) -> dict:
        return super().unstructure() or {}
