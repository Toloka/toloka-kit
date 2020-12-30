from enum import Enum
from typing import Any, Dict, List, Optional

from ..primitives.base import BaseTolokaObject


class DynamicOverlapConfig(BaseTolokaObject):
    """Dynamic overlap setting.

    Allows you to change the overlap depending on how well the performers handle the task.
    Set the closing interval (auto_close_after_complete_delay_seconds). It should be enough to complete tasks
    with an overlap higher than the minimum.
    When all pool tasks are completed, aggregate the responses.
    Attributes:
        type: The algorithm for dynamic overlap.
        max_overlap: Maximum overlap. Must be higher than the values in defaults. Minimum — 1. Maximum — 30000.
        min_confidence: Minimum confidence of the aggregated response. Values from 0 to 1.
        answer_weight_skill_id: A skill that determines the weight of the performer's response. For best results, use
            a skill calculated as percentage of correct responses in control tasks.
        fields: Output data fields to use for aggregating responses.
    """

    class Type(Enum):
        """The algorithm for dynamic overlap.

        BASIC — Each response is assigned a weight depending on the performer's skill value.
            The aggregated response confidence is calculated based on the probability algorithm. The task overlap
            increases until it reaches max_overlap or until the confidence of the aggregated response
            exceeds min_confidence.

            You have to specify max_overlap, min_confidence, answer_weight_skill_id and fields.
        """
        ...

    class Field(BaseTolokaObject):
        """Output data fields to use for aggregating responses.

        For best results, each of these fields must
        have a limited number of response options.
        Don't specify several fields if their values depend on each other.
        Attributes:
            name: The output data field name.
        """

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, name: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        name: Optional[str]

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
        type: Optional[Type] = ...,
        max_overlap: Optional[int] = ...,
        min_confidence: Optional[float] = ...,
        answer_weight_skill_id: Optional[str] = ...,
        fields: Optional[List[Field]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    type: Optional[Type]
    max_overlap: Optional[int]
    min_confidence: Optional[float]
    answer_weight_skill_id: Optional[str]
    fields: Optional[List[Field]]
