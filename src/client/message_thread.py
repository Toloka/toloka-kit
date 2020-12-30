import datetime
from enum import Enum, unique
from typing import Dict, List

from .filter import FilterCondition
from .primitives.base import attribute, BaseTolokaObject


@unique
class RecipientsSelectType(Enum):
    DIRECT = 'DIRECT'
    FILTER = 'FILTER'
    ALL = 'ALL'


@unique
class Folder(Enum):
    INBOX = 'INBOX'
    OUTBOX = 'OUTBOX'
    AUTOMATIC_NOTIFICATION = 'AUTOMATIC_NOTIFICATION'
    IMPORTANT = 'IMPORTANT'
    UNREAD = 'UNREAD'


class Interlocutor(BaseTolokaObject):

    @unique
    class InterlocutorRole(Enum):
        USER = 'USER'
        REQUESTER = 'REQUESTER'
        ADMINISTRATOR = 'ADMINISTRATOR'
        SYSTEM = 'SYSTEM'

    id: str
    role: InterlocutorRole
    myself: bool


class MessageThread(BaseTolokaObject):

    class ComposeDetails(BaseTolokaObject):
        recipients_select_type: RecipientsSelectType
        recipients_ids: List[str]
        recipients_filter: FilterCondition

    class Meta(BaseTolokaObject):
        pool_id: str
        project_id: str
        assignment_id: str

    class Message(BaseTolokaObject):
        text: Dict[str, str]
        from_: Interlocutor = attribute(origin='from')
        created: datetime.datetime

    id: str
    topic: Dict[str, str]
    interlocutors_inlined: bool
    interlocutors: List[Interlocutor]
    messages_inlined: bool
    messages: List[Message]

    meta: Meta
    answerable: bool

    folders: List[Folder]
    compose_details: ComposeDetails

    created: datetime.datetime


class MessageThreadReply(BaseTolokaObject):
    text: Dict[str, str]


class MessageThreadFolders(BaseTolokaObject):
    folders: List[Folder]


class MessageThreadCompose(BaseTolokaObject):
    recipients_select_type: RecipientsSelectType
    topic: Dict[str, str]
    text: Dict[str, str]
    answerable: bool
    recipients_ids: List[str]
    recipients_filter: FilterCondition
