import datetime
from enum import Enum, unique
from typing import Dict, List, Optional

import attr

from .dynamic_overlap_config import DynamicOverlapConfig
from .dynamic_pricing_config import DynamicPricingConfig
from .mixer_config import MixerConfig
from .._converter import unstructure
from ..filter import FilterCondition, FilterOr, FilterAnd
from ..owner import Owner
from ..primitives.base import BaseTolokaObject
from ..quality_control import QualityControl
from ..util._codegen import codegen_attr_attributes_setters, create_setter, expand


@codegen_attr_attributes_setters
class Pool(BaseTolokaObject):

    class AssignmentsIssuingConfig(BaseTolokaObject, kw_only=False):
        issue_task_suites_in_creation_order: bool

    @unique
    class CloseReason(Enum):
        MANUAL = 'MANUAL'
        EXPIRED = 'EXPIRED'
        COMPLETED = 'COMPLETED'
        NOT_ENOUGH_BALANCE = 'NOT_ENOUGH_BALANCE'
        ASSIGNMENTS_LIMIT_EXCEEDED = 'ASSIGNMENTS_LIMIT_EXCEEDED'
        BLOCKED = 'BLOCKED'
        FOR_UPDATE = 'FOR_UPDATE'

    class Defaults(BaseTolokaObject):
        default_overlap_for_new_task_suites: int
        default_overlap_for_new_tasks: int

    @unique
    class Status(Enum):
        OPEN = 'OPEN'
        CLOSED = 'CLOSED'
        ARCHIVED = 'ARCHIVED'
        LOCKED = 'LOCKED'

    class TrainingConfig(BaseTolokaObject, kw_only=False):
        training_skill_ttl_days: int

    @unique
    class Type(Enum):
        REGULAR = 'REGULAR'
        TRAINING = 'TRAINING'

    DynamicOverlapConfig = DynamicOverlapConfig
    DynamicPricingConfig = DynamicPricingConfig
    MixerConfig = MixerConfig
    QualityControl = QualityControl

    project_id: str
    private_name: str
    may_contain_adult_content: bool
    reward_per_assignment: float
    assignment_max_duration_seconds: int
    defaults: Defaults

    will_expire: datetime.datetime

    private_comment: str
    public_description: str
    public_instructions: str
    auto_close_after_complete_delay_seconds: int
    dynamic_pricing_config: DynamicPricingConfig

    auto_accept_solutions: bool
    auto_accept_period_day: int
    assignments_issuing_config: AssignmentsIssuingConfig
    priority: int
    filter: FilterCondition
    quality_control: QualityControl = attr.attrib(factory=QualityControl)
    dynamic_overlap_config: DynamicOverlapConfig
    mixer_config: MixerConfig
    training_config: TrainingConfig

    metadata: Dict[str, List[str]]
    owner: Owner

    # Readonly
    id: str
    status: Status
    last_close_reason: CloseReason
    created: datetime.datetime
    last_started: datetime.datetime
    last_stopped: datetime.datetime
    type: Type

    def unstructure(self) -> Optional[dict]:
        self_unstructured_dict = super().unstructure()
        if self.filter is not None and not isinstance(self.filter, (FilterOr, FilterAnd)):
            self_unstructured_dict['filter'] = unstructure(FilterAnd([self.filter]))
        return self_unstructured_dict

    def is_open(self) -> bool:
        return self.status == Pool.Status.OPEN

    def is_closed(self) -> bool:
        return self.status == Pool.Status.CLOSED

    def is_archived(self) -> bool:
        return self.status == Pool.Status.ARCHIVED

    def is_locked(self) -> bool:
        return self.status == Pool.Status.LOCKED

    set_training_requirement = expand('training_requirement')(create_setter(
        'quality_control.training_requirement',
        QualityControl.TrainingRequirement
    ))

    set_captcha_frequency = expand('captcha_frequency')(create_setter(
        'quality_control.captcha_frequency',
        QualityControl.CaptchaFrequency
    ))

    set_checkpoints_config = expand('checkpoints_config')(create_setter(
        'quality_control.checkpoints_config',
        QualityControl.CheckpointsConfig
    ))

    set_quality_control_configs = create_setter('quality_control.configs')


class PoolPatchRequest(BaseTolokaObject, kw_only=False):
    priority: int
