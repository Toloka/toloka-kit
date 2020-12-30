from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from .owner import Owner
from .primitives.base import BaseTolokaObject


class Attachment(BaseTolokaObject):
    """Attachment

    Files uploaded by users are saved in Toloka.
    Attributes:
        id: File ID.
        name: File name.
        details: Infomation about the pool, the task, and the user who uploaded the file.
        created: The date when the file was uploaded to Toloka.
        media_type: MIME type of the data.
        owner: Owner
    """

    class Type(Enum):
        ...

    class Details(BaseTolokaObject):
        """Infomation about the pool, the task, and the user who uploaded the file.

        Attributes:
            user_id: ID of the user who uploaded the file.
            assignment_id: ID of the task suite assignment to a user.
            pool_id: Pool ID.
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
            user_id: Optional[str] = ...,
            assignment_id: Optional[str] = ...,
            pool_id: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        user_id: Optional[str]
        assignment_id: Optional[str]
        pool_id: Optional[str]

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
        name: Optional[str] = ...,
        details: Optional[Details] = ...,
        created: Optional[datetime] = ...,
        media_type: Optional[str] = ...,
        owner: Optional[Owner] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    name: Optional[str]
    details: Optional[Details]
    created: Optional[datetime]
    media_type: Optional[str]
    owner: Optional[Owner]

class AssignmentAttachment(Attachment):

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
        name: Optional[str] = ...,
        details: Optional[Attachment.Details] = ...,
        created: Optional[datetime] = ...,
        media_type: Optional[str] = ...,
        owner: Optional[Owner] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    name: Optional[str]
    details: Optional[Attachment.Details]
    created: Optional[datetime]
    media_type: Optional[str]
    owner: Optional[Owner]
