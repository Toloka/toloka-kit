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
    """Interlocutor

    Attributes:
        id: ID of the sender or recipient.
        role: Role of the sender or recipient in Toloka:
            * USER — Performer.
            * REQUESTER
            * ADMINISTRATOR
            * SYSTEM — For messages sent automatically.
        myself: Marks a sender or recipient with your ID. If this is your ID, it is set to true.
    """

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
    """MessageThread

    Attributes:
        id: Message thread ID.
        topic: Message thread title.
        interlocutors_inlined: bool
        interlocutors: List[Interlocutor]
        messages_inlined: Access to message threads:
            * True — The message is available in the messages field.
            * False — The message is available in a separate request.
        messages: List[Message]
        meta: Meta
        answerable: Whether the message can be responded to:
            * True — The performer can respond to the message.
            * False — The performer cannot respond to the message.
        folders: Folders where the thread is located.
        compose_details: For messages that you sent: details of the POST request for creating the message.
        created: Date the first message in the thread was created.
    """

    class ComposeDetails(BaseTolokaObject):
        """For messages that you sent: details of the POST request for creating the message.

        """

        recipients_select_type: RecipientsSelectType
        recipients_ids: List[str]
        recipients_filter: FilterCondition

    class Meta(BaseTolokaObject):
        pool_id: str
        project_id: str
        assignment_id: str

    class Message(BaseTolokaObject):
        """Message in the thread.

        Attributes:
            text: Message text.
            from_: Information about the sender.
            created: Date the message was created.
        """

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
    """MessageThreadCompose

    Attributes:
        recipients_select_type: Method for selecting recipients
        topic: Subject of the message. You can enter the subject in multiple
            languages (the message is sent in the user's language).
        text: Message text. You can enter the text in multiple languages (the message is sent in the user's language)
        answerable: Whether the message can be responded to:
            * True — Users can respond to the message.
            * False — Users can't respond to the message.
        recipients_ids: The list of IDs of users who will receive the message.
        recipients_filter: Filter for selecting recipients.
    """

    recipients_select_type: RecipientsSelectType
    topic: Dict[str, str]
    text: Dict[str, str]
    answerable: bool
    recipients_ids: List[str]
    recipients_filter: FilterCondition
