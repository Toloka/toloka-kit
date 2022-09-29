__all__ = [
    'RecipientsSelectType',
    'Folder',
    'Interlocutor',
    'MessageThread',
    'MessageThreadReply',
    'MessageThreadFolders',
    'MessageThreadCompose'
]
import datetime
from enum import unique
from typing import Dict, List, Optional

from ._converter import unstructure
from .filter import FilterCondition, FilterOr, FilterAnd
from .primitives.base import BaseTolokaObject
from ..util._codegen import attribute
from ..util._extendable_enum import ExtendableStrEnum


@unique
class RecipientsSelectType(ExtendableStrEnum):
    """Method for specifying recipients.

    Attributes:
        DIRECT: specify IDs of Tolokers.
        FILTER: select Tolokers using a filter.
        ALL: send a message to all Tolokers who have tried to complete your tasks at least once.
    """

    DIRECT = 'DIRECT'
    FILTER = 'FILTER'
    ALL = 'ALL'


@unique
class Folder(ExtendableStrEnum):
    """Folders for a thread.
    """

    INBOX = 'INBOX'
    OUTBOX = 'OUTBOX'
    AUTOMATIC_NOTIFICATION = 'AUTOMATIC_NOTIFICATION'
    IMPORTANT = 'IMPORTANT'
    UNREAD = 'UNREAD'


class Interlocutor(BaseTolokaObject):
    """Information about the sender or recipient.

    Attributes:
        id: ID of the sender or recipient.
        role: Role of the sender or recipient in Toloka.
        myself: Marks a sender or recipient with your ID. f the ID belongs to you, the value is specified true.
    """

    @unique
    class InterlocutorRole(ExtendableStrEnum):
        """Role of the sender or recipient in Toloka.

        Attributes:
            USER: A Toloker.
            REQUESTER: A requester.
            ADMINISTRATOR: An administrator.
            SYSTEM: For messages sent automatically.
        """

        USER = 'USER'
        REQUESTER = 'REQUESTER'
        ADMINISTRATOR = 'ADMINISTRATOR'
        SYSTEM = 'SYSTEM'

    id: str
    role: InterlocutorRole = attribute(autocast=True)
    myself: bool


class MessageThread(BaseTolokaObject):
    """Message thread.

    The sent message is added to the new message thread. Until the first response is received the message chain is in
    the folder UNREAD. If there are several addresses in the chain and one of them responds, a new message chain
    will be created
    Attributes:
        id: Message thread ID.
        topic: Message thread title.
        interlocutors_inlined: Access information about the sender and recipients.
            * True - information is available in the field interlocutors.
            * False - information is available on a separate request.
        interlocutors: Information about the sender and recipients, sorted by IDs.
        messages_inlined: Access to message threads:
            * True — The message is available in the messages field.
            * False — The message is available in a separate request.
        messages: Messages in the thread. Sorted by creation date (new first).
        meta: Meta
        answerable: Ability to reply to a message:
            * True — The Toloker can respond to the message.
            * False — The Toloker cannot respond to the message.
        folders: Folders where the thread is located.
        compose_details: For messages that you sent: details of the POST request for creating the message.
        created: The date the first message in the chain was created.
    """

    class ComposeDetails(BaseTolokaObject):
        """For messages that you sent: details of the POST request for creating the message.

        Attributes:
            recipients_select_type: Method for specifying recipients.
            recipients_ids: List of recipients IDs.
            recipients_filter: Condition to filter recipients.
        """

        recipients_select_type: RecipientsSelectType = attribute(autocast=True)
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
    """Reply to message thread.

    Attributes:
        text: Message text. You can provide text in several languages (the message will come in the Toloker's language).
            Format: {"<language RU / EN/TR/ID / FR>": "<message text>"}.
    """

    text: Dict[str, str]


class MessageThreadFolders(BaseTolokaObject):
    """Add a message thread to one or more folders

    Attributes:
        folders: Folders to add/remove a message thread to/from.
    """

    folders: List[Folder]


class MessageThreadCompose(BaseTolokaObject):
    """Sent message to a Toloker.

    Attributes:
        recipients_select_type: Method for specifying recipients
        topic: Post title. You can provide a title in several languages (the message will come in the Toloker's language).
            Format: "<language RU/EN/TR/ID/FR>": "<topic text>".
        text: Message text. You can provide text in several languages (the message will come in the Toloker's language).
            Format: "<language RU/EN/TR/ID/FR>": "<message text>".
        answerable: Ability to reply to a message:
            * True — The Toloker can respond to the message.
            * False — The Toloker can't respond to the message.
        recipients_ids: List of IDs of Tolokers to whom the message will be sent.
        recipients_filter: Filter to select recipients.
    """

    recipients_select_type: RecipientsSelectType = attribute(autocast=True)
    topic: Dict[str, str]
    text: Dict[str, str]
    answerable: bool
    recipients_ids: List[str]
    recipients_filter: FilterCondition

    def unstructure(self) -> Optional[dict]:
        self_unstructured_dict = super().unstructure()
        if self.recipients_filter is not None and not isinstance(self.recipients_filter, (FilterOr, FilterAnd)):
            self_unstructured_dict['recipients_filter'] = unstructure(FilterAnd([self.recipients_filter]))
        return self_unstructured_dict
