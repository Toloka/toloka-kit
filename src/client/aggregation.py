from enum import Enum, unique
from typing import Any, Dict, List

from .primitives.base import BaseTolokaObject


@unique
class AggregatedSolutionType(Enum):
    WEIGHTED_DYNAMIC_OVERLAP = 'WEIGHTED_DYNAMIC_OVERLAP'
    DAWID_SKENE = 'DAWID_SKENE'


class PoolAggregatedSolutionRequest(BaseTolokaObject):

    class Field(BaseTolokaObject):
        name: str

    type: AggregatedSolutionType
    pool_id: str
    answer_weight_skill_id: str
    fields: List[Field]


class TaskAggregatedSolutionRequest(BaseTolokaObject, spec_field='type', spec_enum=AggregatedSolutionType):
    task_id: str
    pool_id: str


class WeightedDynamicOverlapTaskAggregatedSolutionRequest(
    TaskAggregatedSolutionRequest,
    spec_value=AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP
):

    class Field(BaseTolokaObject):
        name: str

    answer_weight_skill_id: str
    fields: List[Field]


class AggregatedSolution(BaseTolokaObject):
    pool_id: str
    task_id: str
    confidence: float
    output_values: Dict[str, Any]
