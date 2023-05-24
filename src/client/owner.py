__all__ = ['Owner']
from .primitives.base import BaseTolokaObject


class Owner(BaseTolokaObject):
    """Information about a requester who created some object.

    Attributes:
        id: The ID of the requester.
        myself: Checks the OAuth token that is used in the request:
                * `True` — An object creator has the same OAuth token.
                * `False` — An object creator has different OAuth token.
        company_id: The ID of the requester's company.
    """

    id: str
    myself: bool
    company_id: str
