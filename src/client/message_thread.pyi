from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from .filter import FilterCondition
from .primitives.base import BaseTolokaObject


class RecipientsSelectType(Enum):
    """Method for specifying recipients.

    * DIRECT - specify user IDs.
    * FILTER - select users using filter.
    * ALL - send a message to all users who have tried to complete your tasks at least once.
    """

    ...

class Folder(Enum):
    """Folders for a thread.
    """

    ...

class Interlocutor(BaseTolokaObject):
    """Information about the sender or recipient.

    Attributes:
        id: ID of the sender or recipient.
        role: Role of the sender or recipient in Toloka.
        myself: Marks a sender or recipient with your ID. f the ID belongs to you, the value is specified true.
    """

    class InterlocutorRole(Enum):
        """Role of the sender or recipient in Toloka.

        * USER — Performer.
        * REQUESTER - Customer.
        * ADMINISTRATOR - Administrator.
        * SYSTEM — For messages sent automatically.
        """

        ...

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
        role: Optional[InterlocutorRole] = ...,
        myself: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    role: Optional[InterlocutorRole]
    myself: Optional[bool]

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
            * True — The performer can respond to the message.
            * False — The performer cannot respond to the message.
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
            recipients_select_type: Optional[RecipientsSelectType] = ...,
            recipients_ids: Optional[List[str]] = ...,
            recipients_filter: Optional[FilterCondition] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        recipients_select_type: Optional[RecipientsSelectType]
        recipients_ids: Optional[List[str]]
        recipients_filter: Optional[FilterCondition]

    class Meta(BaseTolokaObject):

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
            pool_id: Optional[str] = ...,
            project_id: Optional[str] = ...,
            assignment_id: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        pool_id: Optional[str]
        project_id: Optional[str]
        assignment_id: Optional[str]

    class Message(BaseTolokaObject):
        """Message in the thread.

        Attributes:
            text: Message text.
            from_: Information about the sender.
            created: Date the message was created.
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
            text: Optional[Dict[str, str]] = ...,
            from_: Optional[Interlocutor] = ...,
            created: Optional[datetime] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        text: Optional[Dict[str, str]]
        from_: Optional[Interlocutor]
        created: Optional[datetime]

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
        topic: Optional[Dict[str, str]] = ...,
        interlocutors_inlined: Optional[bool] = ...,
        interlocutors: Optional[List[Interlocutor]] = ...,
        messages_inlined: Optional[bool] = ...,
        messages: Optional[List[Message]] = ...,
        meta: Optional[Meta] = ...,
        answerable: Optional[bool] = ...,
        folders: Optional[List[Folder]] = ...,
        compose_details: Optional[ComposeDetails] = ...,
        created: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    topic: Optional[Dict[str, str]]
    interlocutors_inlined: Optional[bool]
    interlocutors: Optional[List[Interlocutor]]
    messages_inlined: Optional[bool]
    messages: Optional[List[Message]]
    meta: Optional[Meta]
    answerable: Optional[bool]
    folders: Optional[List[Folder]]
    compose_details: Optional[ComposeDetails]
    created: Optional[datetime]

class MessageThreadReply(BaseTolokaObject):
    """Reply to message thread.

    Attributes:
        text: Message text. You can provide text in several languages (the message will come in the user's language).
            Format: {"<language RU / EN/TR/ID / FR>": "<message text>"}.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, *, text: Optional[Dict[str, str]] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    text: Optional[Dict[str, str]]

class MessageThreadFolders(BaseTolokaObject):
    """Add a message thread to one or more folders

    Attributes:
        folders: Folders to add/remove a message thread to/from.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, *, folders: Optional[List[Folder]] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    folders: Optional[List[Folder]]

class MessageThreadCompose(BaseTolokaObject):
    """Sent message to perfromer

    Attributes:
        recipients_select_type: Method for specifying recipients
        topic: Post title. You can provide a title in several languages (the message will come in the user's language).
            Format: "<language RU/EN/TR/ID/FR>": "<topic text>".
        text: Message text. You can provide text in several languages (the message will come in the user's language).
            Format: "<language RU/EN/TR/ID/FR>": "<message text>".
        answerable: Ability to reply to a message:
            * True — Users can respond to the message.
            * False — Users can't respond to the message.
        recipients_ids: List of IDs of users to whom the message will be sent.
        recipients_filter: Filter to select recipients.
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
        recipients_select_type: Optional[RecipientsSelectType] = ...,
        topic: Optional[Dict[str, str]] = ...,
        text: Optional[Dict[str, str]] = ...,
        answerable: Optional[bool] = ...,
        recipients_ids: Optional[List[str]] = ...,
        recipients_filter: Optional[FilterCondition] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    recipients_select_type: Optional[RecipientsSelectType]
    topic: Optional[Dict[str, str]]
    text: Optional[Dict[str, str]]
    answerable: Optional[bool]
    recipients_ids: Optional[List[str]]
    recipients_filter: Optional[FilterCondition]
