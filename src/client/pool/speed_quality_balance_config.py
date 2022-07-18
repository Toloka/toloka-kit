__all__ = [
    'SpeedQualityBalanceConfig',
    'TopPercentageByQuality',
    'BestConcurrentUsersByQuality',
]
from enum import unique
from ..primitives.base import BaseTolokaObject
from ...util._extendable_enum import ExtendableStrEnum


class SpeedQualityBalanceConfig(BaseTolokaObject, spec_enum='Type', spec_field='type'):
    """Adjust balance between speed and quality.
    """

    @unique
    class Type(ExtendableStrEnum):
        """The type of speed quality balance:

        Attributes:
            TOP_PERCENTAGE_BY_QUALITY: get top XX% Tolokers by quality.
            BEST_CONCURRENT_USERS_BY_QUALITY: get top x Tolokers by quality.
        """
        TOP_PERCENTAGE_BY_QUALITY = 'TOP_PERCENTAGE_BY_QUALITY'
        BEST_CONCURRENT_USERS_BY_QUALITY = 'BEST_CONCURRENT_USERS_BY_QUALITY'


class TopPercentageByQuality(SpeedQualityBalanceConfig,
                             spec_value=SpeedQualityBalanceConfig.Type.TOP_PERCENTAGE_BY_QUALITY):
    """The percentage of Tolokers ordered by quality that will work on pool.
    """
    percent: int


class BestConcurrentUsersByQuality(SpeedQualityBalanceConfig,
                                   spec_value=SpeedQualityBalanceConfig.Type.BEST_CONCURRENT_USERS_BY_QUALITY):
    """How many concurrent Tolokers ordered by quality will work on pool.
    """
    count: int
