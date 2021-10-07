__all__ = [
    'MetricCollector',
]
import toloka.metrics.metrics
import typing


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

    def __init__(self, metrics: typing.List[toloka.metrics.metrics.BaseMetric]): ...

    def get_lines(self) -> typing.Dict[str, typing.List[typing.Tuple[typing.Any, typing.Any]]]: ...

    metrics: typing.List[toloka.metrics.metrics.BaseMetric]
