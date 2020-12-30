from enum import Enum, unique
from typing import List

from ..primitives.base import BaseTolokaObject


class DynamicOverlapConfig(BaseTolokaObject):

    @unique
    class Type(Enum):
        BASIC = 'BASIC'

    class Field(BaseTolokaObject, kw_only=False):
        name: str

    type: Type
    max_overlap: int
    min_confidence: float
    answer_weight_skill_id: str
    fields: List[Field]
