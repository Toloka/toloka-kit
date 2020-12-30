from enum import Enum, unique
from typing import List

from .actions import RuleAction
from .collectors import CollectorConfig
from .conditions import RuleCondition
from .primitives.base import attribute, BaseTolokaObject
from .task_distribution_function import TaskDistributionFunction


class QualityControl(BaseTolokaObject):

    class TrainingRequirement(BaseTolokaObject):
        training_pool_id: str
        training_passing_skill_value: int

    @unique
    class CaptchaFrequency(Enum):
        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'

    class CheckpointsConfig(BaseTolokaObject):

        class Settings(BaseTolokaObject):
            target_overlap: int
            task_distribution_function: TaskDistributionFunction

        real_settings: Settings
        golden_settings: Settings
        training_settings: Settings

    class QualityControlConfig(BaseTolokaObject):

        class RuleConfig(BaseTolokaObject):
            action: RuleAction
            conditions: List[RuleCondition]

        rules: List[RuleConfig]
        collector_config: CollectorConfig

    training_requirement: TrainingRequirement
    captcha_frequency: CaptchaFrequency
    configs: List[QualityControlConfig] = attribute(factory=list)
    checkpoints_config: CheckpointsConfig

    def add_action(self, collector: CollectorConfig, action: RuleAction, conditions: List[RuleCondition]):
        # Checking that conditions are compatible with our collector
        collector.validate_condition(conditions)

        # We can possibly add the action to an existing config
        for config in self.configs:
            if config.collector_config == collector:
                break
        else:
            config = QualityControl.QualityControlConfig(rules=[], collector_config=collector)
            self.configs.append(config)

        rule = QualityControl.QualityControlConfig.RuleConfig(action=action, conditions=conditions)
        config.rules.append(rule)
