from enum import Enum
from typing import Any, Dict, List, Optional

from .primitives.base import BaseTolokaObject


class AggregatedSolutionType(Enum):
    ...

class PoolAggregatedSolutionRequest(BaseTolokaObject):
    """PoolAggregatedSolutionRequest

    Attributes:
        type: Aggregation type. WEIGHTED_DYNAMIC_OVERLAP — Aggregation of responses in a pool with dynamic overlap.
        pool_id: Pool ID.
        answer_weight_skill_id: A skill that determines the weight of the performer's response.
        fields: Output data fields to use for aggregating responses. For best results, each of these fields
            must have a limited number of response options.
    """

    class Field(BaseTolokaObject):
        """Field

        Output data fields to use for aggregating responses. For best results, each of these fields must
        have a limited number of response options.
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

        def __init__(self, *, name: Optional[str] = ...) -> None: ...

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
        type: Optional[AggregatedSolutionType] = ...,
        pool_id: Optional[str] = ...,
        answer_weight_skill_id: Optional[str] = ...,
        fields: Optional[List[Field]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    type: Optional[AggregatedSolutionType]
    pool_id: Optional[str]
    answer_weight_skill_id: Optional[str]
    fields: Optional[List[Field]]

class TaskAggregatedSolutionRequest(BaseTolokaObject):
    """TaskAggregatedSolutionRequest

    Attributes:
        task_id: Task ID.
        pool_id: Pool ID.
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
        task_id: Optional[str] = ...,
        pool_id: Optional[str] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    task_id: Optional[str]
    pool_id: Optional[str]

class WeightedDynamicOverlapTaskAggregatedSolutionRequest(TaskAggregatedSolutionRequest):
    """WeightedDynamicOverlapTaskAggregatedSolutionRequest

    Attributes:
        answer_weight_skill_id: A skill that determines the weight of the performer's response.
        fields: Output data fields to use for aggregating responses. For best results, each of these fields
            must have a limited number of response options.
    """

    class Field(BaseTolokaObject):
        """Field

        Output data fields to use for aggregating responses. For best results, each of these fields must
        have a limited number of response options.
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

        def __init__(self, *, name: Optional[str] = ...) -> None: ...

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
        task_id: Optional[str] = ...,
        pool_id: Optional[str] = ...,
        answer_weight_skill_id: Optional[str] = ...,
        fields: Optional[List[Field]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    task_id: Optional[str]
    pool_id: Optional[str]
    answer_weight_skill_id: Optional[str]
    fields: Optional[List[Field]]

class AggregatedSolution(BaseTolokaObject):
    """Contains the aggregated task response.

    Attributes:
        pool_id: Pool ID.
        task_id: Task ID.
        confidence: Confidence in the aggregate response.
        output_values: Output data fields and aggregate response.
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
        pool_id: Optional[str] = ...,
        task_id: Optional[str] = ...,
        confidence: Optional[float] = ...,
        output_values: Optional[Dict[str, Any]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    pool_id: Optional[str]
    task_id: Optional[str]
    confidence: Optional[float]
    output_values: Optional[Dict[str, Any]]
