__all__ = [
    'Balance',
    'AssignmentEventsInPool',
    'AssignmentsInPool',
]

import datetime
from itertools import groupby
from operator import attrgetter

import attr
from typing import Any, Optional, Dict, List, Tuple
from ..client import (
    Requester,
    TolokaClient,
)
from ..client import analytics_request
from ..client.operations import Operation
from ..client._converter import structure
from ..streaming import cursor


class BaseMetric:
    def get_metrics(self, toloka_client: TolokaClient) -> Dict[str, List[Tuple[Any, Any]]]:
        """Gather and return metrics

        All metrics returned in the same format: named list, contain pairs of: datetime of some event, metric value.
        Could not return some metrics in dict on iteration or return it with empty list:
        means that is nothing being gathered on this step. This is not zero value!

        Return example:
        {
            'rejected_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 44, 895232), 0)],
            'submitted_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 45, 321904), 75)],
            'accepted_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 45, 951156), 75)],
            'accepted_events_in_pool': [(datetime.datetime(2021, 8, 11, 15, 13, 3, 65000), 1), ... ],
            'rejected_events_in_pool': [],
            # no toloka_requester_balance on this iteration
        }
        """
        raise NotImplementedError


@attr.s(auto_attribs=True)
class AssignmentEventsInPool(BaseMetric):
    """Tracking the change of response statuses in the pool.
    The metric is convenient for tracking that the pool is generally "alive" and working.
    If you want to track assignments counts, it's better to use AssignmentsInPool.

    Metrics starts gathering if they name are set. If the metric name is set to None, they don't gathering.

    Args:
        pool_id: From which pool track metrics.
        created_name: Metric name for a count of created events. Default None.
        submitted_name: Metric name for a count of submitted events. Default 'submitted_events_in_pool'.
        accepted_name : Metric name for a count of accepted events. Default 'accepted_events_in_pool'.
        rejected_name : Metric name for a count of rejected events. Default 'rejected_events_in_pool'.
        skipped_name: Metric name for a count of skipped events. Default None.
        expired_name: Metric name for a count of expired events. Default None.
        join_events: Count all events in one point.  Default False.

    Raises:
        ValueError: If all metric names are set to None or if there are duplicate metric names.

    Example:
        How to collect this metrics:
        >>> collector = MetricCollector(toloka_client, AssignmentEventsInPool(pool_id))
        >>> metric_dict = collector.get_metrics()
        {
            'submitted_events_in_pool': [(datetime.datetime(2021, 8, 11, 15, 13, 4, 31000), 5)],
            'accepted_events_in_pool': [(datetime.datetime(2021, 8, 11, 15, 13, 3, 65000), 1)],
            'rejected_events_in_pool': [],
        }
    """
    pool_id : str = attr.ib(kw_only=False)
    created_name : Optional[str] = None
    submitted_name : Optional[str] = 'submitted_events_in_pool'
    accepted_name : Optional[str] = 'accepted_events_in_pool'
    rejected_name : Optional[str] = 'rejected_events_in_pool'
    skipped_name : Optional[str] = None
    expired_name : Optional[str] = None

    join_events : bool = False

    # key - metric name. One of the value of paramets: created_name, submitted_name, etc.
    # val - cursor configured for gathering this metric
    _cursors : Dict[str, cursor.AssignmentCursor] = attr.Factory(dict)

    STATUS_DICT = {
        'created_name': 'CREATED',
        'submitted_name': 'SUBMITTED',
        'accepted_name': 'ACCEPTED',
        'rejected_name': 'REJECTED',
        'skipped_name': 'SKIPPED',
        'expired_name': 'EXPIRED',
    }

    def _create_cursors(self, toloka_client: TolokaClient) -> None:

        start_time = datetime.datetime.utcnow()
        for attr_name, status_value in self.STATUS_DICT.items():
            metric_name = getattr(self, attr_name)
            if metric_name:
                if metric_name in self._cursors:
                    raise ValueError(f'Duplicate metric names: "{metric_name}"')
                self._cursors[metric_name] = cursor.AssignmentCursor(
                    pool_id=self.pool_id,
                    event_type=status_value,
                    toloka_client=toloka_client,
                    **{f'{status_value.lower()}_gte': start_time}
                )
        if not self._cursors:
            raise ValueError('No cursors were created in AssignmentsInPool. Check that any "*_name" was settled.')

    def get_metrics(self, toloka_client: TolokaClient) -> Dict[str, List[Tuple[Any, Any]]]:
        if not self._cursors:
            self._create_cursors(toloka_client)
        result = {}
        for metric_name, it in self._cursors.items():
            if self.join_events:
                event_list = list(it)
                result[metric_name] = [(event_list[-1].event_time, len(event_list))] if event_list else []
            else:
                result[metric_name] = [
                    (event_time, len(events))
                    for event_time, events in groupby(it, attrgetter('event_time'))
                ]
        return result


@attr.s(auto_attribs=True)
class AssignmentsInPool(BaseMetric):
    """Tracking the count of assignments in different states in the pool.

    Metrics starts gathering if they name are set. If the metric name is set to None, they don't gathering.
    This metric could "skip" get_metrics and return an empty list if the inner operation was still in progress.

    Args:
        pool_id: From which pool track metrics.
        submitted_name: Metric name for a count of submitted assignments. Default 'submitted_assignments_in_pool'.
        accepted_name : Metric name for a count of accepted assignments. Default 'accepted_assignments_in_pool'.
        rejected_name : Metric name for a count of rejected assignments. Default 'rejected_assignments_in_pool'.
        skipped_name: Metric name for a count of skipped assignments. Default None.

    Raises:
        ValueError: If all metric names are set to None.

    Example:
        How to collect this metrics:
        >>> collector = MetricCollector(toloka_client, AssignmentsInPool(pool_id))
        >>> metric_dict = collector.get_metrics()
        {
            'rejected_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 44, 895232), 0)],
            'submitted_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 45, 321904), 75)],
            'accepted_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 45, 951156), 75)],
        }
    """
    pool_id : str = attr.ib(kw_only=False)
    submitted_name : Optional[str] = 'submitted_assignments_in_pool'
    accepted_name : Optional[str] = 'accepted_assignments_in_pool'
    rejected_name : Optional[str] = 'rejected_assignments_in_pool'
    skipped_name : Optional[str] = None

    _analytics_for_request : List[analytics_request.PoolAnalyticsRequest] = attr.Factory(list)
    _previous_operation : Optional[Operation] = None

    ANALYTICS_DICT = {
        'submitted_name': analytics_request.SubmitedAssignmentsCountPoolAnalytics,
        'accepted_name': analytics_request.ApprovedAssignmentsCountPoolAnalytics,
        'rejected_name': analytics_request.RejectedAssignmentsCountPoolAnalytics,
        'skipped_name': analytics_request.SkippedAssignmentsCountPoolAnalytics,
    }

    def get_metrics(self, toloka_client: TolokaClient) -> Dict[str, List[Tuple[Any, Any]]]:
        field_names = {str(analytic_class.name.value): field_name for field_name, analytic_class in self.ANALYTICS_DICT.items()}

        if not self._analytics_for_request:
            for attr_name, analytic in self.ANALYTICS_DICT.items():
                attr_val = getattr(self, attr_name)
                if attr_val:
                    self._analytics_for_request.append(analytic(subject_id=self.pool_id))
            if not self._analytics_for_request:
                raise ValueError('No analytics request was created. Check that any "*_name" was set.')

        result = {}
        if self._previous_operation is not None:
            operation = toloka_client.get_operation(self._previous_operation.id)
            if not operation.is_completed():
                return result
            if operation.status == Operation.Status.SUCCESS:
                for response in operation.details['value']:
                    metric_name = response['request']['name']
                    metric_name = field_names[metric_name]
                    metric_name = getattr(self, metric_name)
                    result[metric_name] = [(structure(response['finished'], datetime.datetime), response['result'])]

        self._previous_operation = toloka_client.get_analytics(self._analytics_for_request)
        return result


@attr.s(auto_attribs=True)
class Balance(BaseMetric):
    """Traking your Toloka balance.

    Returns only one metric: don't spend and don't reserved money on your acount.

    Args:
        balance_name: Metric name. Default 'toloka_requester_balance'.

    Raises:
        ValueError: If all metric names are set to None.

    Example:
        How to collect this metrics:
        >>> collector = MetricCollector(toloka_client, Balance())
        >>> metric_dict = collector.get_metrics()
        {
            toloka_requester_balance: [(datetime.datetime(2021, 8, 30, 10, 30, 59, 628239), Decimal('123.4500'))],
        }
    """

    balance_name : Optional[str] = 'toloka_requester_balance'

    def get_metrics(self, toloka_client: TolokaClient) -> Dict[str, List[Tuple[Any, Any]]]:
        if not self.balance_name:
            raise ValueError('"balance_name" must be set')
        result = {}
        requester: Requester = toloka_client.get_requester()
        result[self.balance_name] = [(datetime.datetime.utcnow(), requester.balance)]
        return result
