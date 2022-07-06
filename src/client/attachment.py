__all__ = [
    'Attachment',
    'AssignmentAttachment'
]

import datetime
from enum import unique

from .owner import Owner
from .primitives.base import BaseTolokaObject
from ..util._docstrings import inherit_docstrings
from ..util._extendable_enum import ExtendableStrEnum


class Attachment(BaseTolokaObject, spec_enum='Type', spec_field='attachment_type'):
    """Attachment

    Files uploaded by Tolokers are saved in Toloka.
    Attributes:
        id: File ID.
        name: File name.
        details: Information about the pool, the task, and the Toloker who uploaded the file.
        created: Date the file was uploaded to Toloka.
        media_type: MIME data type.
        owner: Owner
    """

    @unique
    class Type(ExtendableStrEnum):
        ASSIGNMENT_ATTACHMENT = 'ASSIGNMENT_ATTACHMENT'

    ASSIGNMENT_ATTACHMENT = Type.ASSIGNMENT_ATTACHMENT

    class Details(BaseTolokaObject):
        """Information about the pool, task, and the Toloker from which the file was received.

        Attributes:
            user_id: ID of the Toloker from whom the file was received.
            assignment_id: ID for issuing a set of tasks to the Toloker.
            pool_id: Pool ID.
        """

        user_id: str
        assignment_id: str
        pool_id: str

    id: str
    name: str
    details: Details
    created: datetime.datetime
    media_type: str

    owner: Owner


@inherit_docstrings
class AssignmentAttachment(Attachment, spec_value=Attachment.Type.ASSIGNMENT_ATTACHMENT):
    """Assignment Attachment.
    """

    pass
