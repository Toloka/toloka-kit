__all__ = [
    'MetricCollector',
]

import logging

from typing import Any, Dict, List, Tuple

from ..client import (
    Requester,
    TolokaClient,
)
from .metrics import BaseMetric

logger = logging.getLogger(__name__)


class MetricCollector:
    """Gather metrics

    Raises:
        TypeError: If toloka_client param isn't instance of toloka.clien.TolokaClient
        TypeError: If some of other positional arguments isn't instance of toloka.metrics.BaseMetric

    Example:
        How to gather metrics and sends it to zabbix:

        >>> import toloka.client as toloka
        >>> from toloka.metrics import MetricCollector, Balance, Delta, AssignmentsInPool, MessagesInPool
        >>>
        >>> toloka_client = toloka.TolokaClient(auth_token, 'PRODUCTION')
        >>>
        >>> collector = MetricCollector(
        >>>     toloka_client,
        >>>     [
        >>>         Balance(),
        >>>         AssignmentsInPool(pool_id),
        >>>     ],
        >>> )
        >>>
        >>> while True:
        >>>     metric_dict = collector.get_metrics()
        >>>     send_metric_to_zabbix(metric_dict)
        >>>     sleep(10)
    """

    toloka_client : TolokaClient
    metrics : List[BaseMetric]

    def __init__(self, toloka_client: TolokaClient, metrics: List[BaseMetric]):
        if not isinstance(toloka_client, TolokaClient):
            raise TypeError('"toloka_client" must be an instance of toloka.client.TolokaClient')
        self.toloka_client = toloka_client
        requester: Requester = self.toloka_client.get_requester()
        logger.info(f'Metrics will be gather for requester: "{requester.public_name}", company: "{requester.company}"')
        self.metrics = []
        for i, element in enumerate(metrics):
            if not isinstance(element, BaseMetric):
                raise TypeError(f'{i+1} positional argument must be an instance of toloka.metrics.BaseMetric, now it\'s {type(element)}')
            self.metrics.append(element)

    def get_metrics(self) -> Dict[str, List[Tuple[Any, Any]]]:
        result = {}
        for metric in self.metrics:
            new_points = metric.get_metrics(self.toloka_client)
            for name, points in new_points.items():
                if name in result:
                    logger.warning(f'Duplicated metrics name detected: "{name}". Only one metric was returned.')
                result[name] = points
        return result
