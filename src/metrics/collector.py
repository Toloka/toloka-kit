__all__ = [
    'MetricCollector',
]

import logging

from typing import Any, Dict, List, Tuple

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
        >>> from toloka.metrics import AssignmentsInPool, Balance, bind_client, MetricCollector
        >>>
        >>> toloka_client = toloka.TolokaClient(auth_token, 'PRODUCTION')
        >>>
        >>> collector = MetricCollector(
        >>>     [
        >>>         Balance(),
        >>>         AssignmentsInPool(pool_id),
        >>>     ],
        >>> )
        >>> bind_client(collector.metrics, toloka_client)
        >>>
        >>> while True:
        >>>     metric_dict = collector.get_lines()
        >>>     send_metric_to_zabbix(metric_dict)
        >>>     sleep(10)
    """

    metrics : List[BaseMetric]

    def __init__(self, metrics: List[BaseMetric]):
        self.metrics = []
        for i, element in enumerate(metrics):
            if not isinstance(element, BaseMetric):
                raise TypeError(f'{i+1} positional argument must be an instance of toloka.metrics.BaseMetric, now it\'s {type(element)}')
            self.metrics.append(element)

    def get_lines(self) -> Dict[str, List[Tuple[Any, Any]]]:
        result = {}
        for metric in self.metrics:
            new_points = metric.get_lines()
            for name, points in new_points.items():
                if name in result:
                    logger.warning(f'Duplicated metrics name detected: "{name}". Only one metric was returned.')
                result[name] = points
        return result
