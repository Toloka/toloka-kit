__all__ = ['Owner']
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

    id: str
    myself: bool
    company_id: str
