import datetime
from enum import Enum, unique

from .owner import Owner
from .primitives.base import BaseTolokaObject


class Attachment(BaseTolokaObject, spec_enum='Type', spec_field='attachment_type'):

    @unique
    class Type(Enum):
        ASSIGNMENT_ATTACHMENT = 'ASSIGNMENT_ATTACHMENT'

    ASSIGNMENT_ATTACHMENT = Type.ASSIGNMENT_ATTACHMENT

    class Details(BaseTolokaObject):
        user_id: str
        assignment_id: str
        pool_id: str

    id: str
    name: str
    details: Details
    created: datetime.datetime
    media_type: str

    owner: Owner


class AssignmentAttachment(Attachment, spec_value=Attachment.Type.ASSIGNMENT_ATTACHMENT):
    pass
