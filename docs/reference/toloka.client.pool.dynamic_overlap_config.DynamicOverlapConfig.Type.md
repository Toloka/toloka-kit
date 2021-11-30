# Type
`toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig.Type`

The algorithm for dynamic overlap.


Atttributes:
    BASIC: Each response is assigned a weight depending on the performer's skill value.
        The aggregated response confidence is calculated based on the probability algorithm. The task overlap
        increases until it reaches max_overlap or until the confidence of the aggregated response
        exceeds min_confidence.
        You have to specify max_overlap, min_confidence, answer_weight_skill_id and fields.

## Attributes Description

| Name | Value | Description |
| :------| :-----------| :----------| 
`BASIC`|'BASIC'|<p></p>
