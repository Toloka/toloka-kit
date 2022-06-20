# EventType
`toloka.client.webhook_subscription.WebhookSubscription.EventType` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/webhook_subscription.py#L22)

Webhook subscription event type:

## Attributes Description

| Name | Value | Description |
| :------| :-----------| :----------| 
`POOL_CLOSED`|'POOL_CLOSED'|<p>The pool is closed.</p>
`DYNAMIC_OVERLAP_COMPLETED`|'DYNAMIC_OVERLAP_COMPLETED'|<p>There is an aggregated estimate for dynamic overlap.</p>
`ASSIGNMENT_CREATED`|'ASSIGNMENT_CREATED'|<p>Task created.</p>
`ASSIGNMENT_SUBMITTED`|'ASSIGNMENT_SUBMITTED'|<p>The task has been completed and is waiting for acceptance by the customer.</p>
`ASSIGNMENT_SKIPPED`|'ASSIGNMENT_SKIPPED'|<p>The task was taken to work, but the performer missed it and will not return to it.</p>
`ASSIGNMENT_EXPIRED`|'ASSIGNMENT_EXPIRED'|<p>The task was taken to work, but the performer did not have time to complete it in the allotted time or refused it before the end of the term.</p>
`ASSIGNMENT_APPROVED`|'ASSIGNMENT_APPROVED'|<p>The task was performed by the performer and confirmed by the customer.</p>
`ASSIGNMENT_REJECTED`|'ASSIGNMENT_REJECTED'|<p>The task was completed by the performer, but rejected by the customer.</p>
