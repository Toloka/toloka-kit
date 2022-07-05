__all__ = ['DynamicOverlapConfig']
from enum import unique
from typing import List

from ..primitives.base import BaseTolokaObject
from ...util._codegen import attribute
from ...util._extendable_enum import ExtendableStrEnum


class DynamicOverlapConfig(BaseTolokaObject):
    """Dynamic overlap setting.

    Allows you to change the overlap depending on how well Tolokers handle the task.
    Set the closing interval (auto_close_after_complete_delay_seconds). It should be enough to complete tasks
    with an overlap higher than the minimum.
    When all pool tasks are completed, aggregate the responses.
    Attributes:
        type: The algorithm for dynamic overlap.
        max_overlap: Maximum overlap. Must be higher than the values in defaults. Minimum — 1. Maximum — 30000.
        min_confidence: Minimum confidence of the aggregated response. Values from 0 to 1.
        answer_weight_skill_id: A skill that determines the weight of the Toloker's response. For best results, use
            a skill calculated as percentage of correct responses in control tasks.
        fields: Output data fields to use for aggregating responses.
    """

    @unique
    class Type(ExtendableStrEnum):
        """The algorithm for dynamic overlap.

        Attributes:
            BASIC: Each response is assigned a weight depending on the Toloker's skill value.
                The aggregated response confidence is calculated based on the probability algorithm. The task overlap
                increases until it reaches max_overlap or until the confidence of the aggregated response
                exceeds min_confidence.
                You have to specify max_overlap, min_confidence, answer_weight_skill_id and fields.
        """

        BASIC = 'BASIC'

    class Field(BaseTolokaObject, kw_only=False):
        """Output data fields to use for aggregating responses.

        For best results, each of these fields must
        have a limited number of response options.
        Don't specify several fields if their values depend on each other.
        Attributes:
            name: The output data field name.
        """

        name: str

    type: Type = attribute(autocast=True)
    max_overlap: int
    min_confidence: float
    answer_weight_skill_id: str
    fields: List[Field]
