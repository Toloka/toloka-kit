__all__ = [
    'WebhookSubscription',
]
from datetime import datetime
from enum import unique

from .primitives.base import BaseTolokaObject
from ..util._codegen import attribute
from ..util._extendable_enum import ExtendableStrEnum


class WebhookSubscription(BaseTolokaObject):
    """Webhook subscription to make a callback to the given address when some event happen.

    Attributes:
        webhook_url: The URL to which notifications will be sent.
        event_type: Event type.
        pool_id: ID of the pool for which the subscription was created.
        id: Pool ID. Read only field.
        created: When this pool was created. Read only field.
    """

    @unique
    class EventType(ExtendableStrEnum):
        """Webhook subscription event type:

        Attributes:
            POOL_CLOSED: The pool is closed.
            DYNAMIC_OVERLAP_COMPLETED: There is an aggregated estimate for dynamic overlap.
            ASSIGNMENT_CREATED: Task created.
            ASSIGNMENT_SUBMITTED: The task has been completed and is waiting for acceptance by the customer.
            ASSIGNMENT_SKIPPED: The task was taken to work, but the performer missed it and will not return to it.
            ASSIGNMENT_EXPIRED: The task was taken to work, but the performer did not have time to complete it in the allotted time or refused it before the end of the term.
            ASSIGNMENT_APPROVED: The task was performed by the performer and confirmed by the customer.
            ASSIGNMENT_REJECTED: The task was completed by the performer, but rejected by the customer.
        """

        POOL_CLOSED = 'POOL_CLOSED'
        DYNAMIC_OVERLAP_COMPLETED = 'DYNAMIC_OVERLAP_COMPLETED'
        ASSIGNMENT_CREATED = 'ASSIGNMENT_CREATED'
        ASSIGNMENT_SUBMITTED = 'ASSIGNMENT_SUBMITTED'
        ASSIGNMENT_SKIPPED = 'ASSIGNMENT_SKIPPED'
        ASSIGNMENT_EXPIRED = 'ASSIGNMENT_EXPIRED'
        ASSIGNMENT_APPROVED = 'ASSIGNMENT_APPROVED'
        ASSIGNMENT_REJECTED = 'ASSIGNMENT_REJECTED'

    webhook_url: str
    event_type: EventType = attribute(autocast=True)
    pool_id: str
    secret_key: str

    # Readonly
    id: str = attribute(readonly=True)
    created: datetime = attribute(readonly=True)
