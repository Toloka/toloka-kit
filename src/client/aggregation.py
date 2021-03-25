__all__ = [
    'AggregatedSolutionType',
    'PoolAggregatedSolutionRequest',
    'TaskAggregatedSolutionRequest',
    'WeightedDynamicOverlapTaskAggregatedSolutionRequest',
    'AggregatedSolution'
]
from enum import Enum, unique
from typing import Any, Dict, List

from .primitives.base import BaseTolokaObject


@unique
class AggregatedSolutionType(Enum):
    WEIGHTED_DYNAMIC_OVERLAP = 'WEIGHTED_DYNAMIC_OVERLAP'
    DAWID_SKENE = 'DAWID_SKENE'


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

        name: str

    type: AggregatedSolutionType
    pool_id: str
    answer_weight_skill_id: str
    fields: List[Field]


class TaskAggregatedSolutionRequest(BaseTolokaObject, spec_field='type', spec_enum=AggregatedSolutionType):
    """TaskAggregatedSolutionRequest

    Attributes:
        task_id: Task ID.
        pool_id: Pool ID.
    """

    task_id: str
    pool_id: str


class WeightedDynamicOverlapTaskAggregatedSolutionRequest(
    TaskAggregatedSolutionRequest,
    spec_value=AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP
):
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

        name: str

    answer_weight_skill_id: str
    fields: List[Field]


class AggregatedSolution(BaseTolokaObject):
    """Contains the aggregated task response.

    Attributes:
        pool_id: Pool ID.
        task_id: Task ID.
        confidence: Confidence in the aggregate response.
        output_values: Output data fields and aggregate response.
    """

    pool_id: str
    task_id: str
    confidence: float
    output_values: Dict[str, Any]
