# CloseReason
`toloka.client.training.Training.CloseReason` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/training.py#L49)

The reason for closing the pool the last time:

## Attributes Description

| Name | Value | Description |
| :------| :-----------| :----------| 
`MANUAL`|'MANUAL'|<p>Closed by the requester.</p>
`EXPIRED`|'EXPIRED'|<p>Reached the date and time set in will_expire.</p>
`COMPLETED`|'COMPLETED'|<p>Closed automatically because all the pool tasks were completed.</p>
`NOT_ENOUGH_BALANCE`|'NOT_ENOUGH_BALANCE'|<p>Closed automatically because the Toloka account ran out of funds.</p>
`ASSIGNMENTS_LIMIT_EXCEEDED`|'ASSIGNMENTS_LIMIT_EXCEEDED'|<p>Closed automatically because it exceeded the limit on assigned task suites (maximum of 2 million).</p>
`BLOCKED`|'BLOCKED'|<p>Closed automatically because the requester&#x27;s account was blocked by a Toloka administrator.</p>
`FOR_UPDATE`|'FOR_UPDATE'|<p></p>
