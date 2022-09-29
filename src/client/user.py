__all__ = [
    'User',
]

from typing import List

from .primitives.base import BaseTolokaObject


class User(BaseTolokaObject):
    """Toloker metadata.

    Attributes:
        id: Toloker ID.
        country: Toloker country code.
        languages: list of languages that Toloker know represented with language codes.
        adult_allowed: shows whether Toloker agreed to complete tasks with adult content.
        attributes: Toloker attributes.
    """

    class Attributes(BaseTolokaObject):
        country_by_phone: str
        country_by_ip: str
        client_type: str
        user_agent_type: str
        device_category: str
        os_family: str
        os_version: float
        os_version_major: int
        os_version_minor: int
        os_version_bugfix: int

    id: str
    country: str
    languages: List[str]
    adult_allowed: bool
    attributes: Attributes
