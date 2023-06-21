__all__ = [
    'actions',
    'aggregation',
    'analytics_request',
    'app',
    'assignment',
    'attachment',
    'batch_create_results',
    'clone_results',
    'collectors',
    'conditions',
    'error_codes',
    'exceptions',
    'filter',
    'message_thread',
    'operation_log',
    'operations',
    'owner',
    'quality_control',
    'requester',
    'search_requests',
    'search_results',
    'skill',
    'solution',
    'task',
    'task_distribution_function',
    'task_suite',
    'training',
    'user_bonus',
    'user_restriction',
    'user_skill',
    'webhook_subscription',

    'structure',
    'unstructure',

    'TolokaClient',
    'AggregatedSolution',
    'AnalyticsRequest',
    'Assignment',
    'AssignmentPatch',
    'CloneResults',
    'GetAssignmentsTsvParameters',
    'Attachment',
    'Folder',
    'MessageThread',
    'MessageThreadReply',
    'MessageThreadFolders',
    'MessageThreadCompose',
    'OperationLogItem',
    'Requester',
    'Skill',
    'SetUserSkillRequest',
    'TaskSuite',
    'Task',
    'Training',
    'UserBonus',
    'UserRestriction',
    'UserSkill',
    'User',
    'Pool',
    'PoolPatchRequest',
    'Project',
    'AppProject',
    'App',
    'AppItem',
    'AppItemsCreateRequest',
    'AppBatch',
    'AppBatchCreateRequest',
]

import datetime
import functools
import io
import logging
import threading
import time

import attr
import httpx
import simplejson
from httpx import HTTPStatusError
from httpx._types import VerifyTypes
from toloka.client.batch_create_results import FieldValidationError

try:
    import pandas as pd
    PANDAS_INSTALLED = True
except ImportError:
    PANDAS_INSTALLED = False

from decimal import Decimal
from enum import Enum, unique
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from typing import BinaryIO, Callable, ClassVar, Dict, Generator, List, Optional, Sequence, Tuple, Union
from urllib3.util.retry import Retry

from . import actions
from . import aggregation
from . import analytics_request
from . import app
from . import assignment
from . import attachment
from . import batch_create_results
from . import clone_results
from . import collectors
from . import conditions
from . import error_codes
from . import exceptions
from . import filter
from . import message_thread
from . import operation_log
from . import operations
from . import owner
from . import quality_control
from . import requester
from . import search_requests
from . import search_results
from . import skill
from . import solution
from . import task
from . import task_distribution_function
from . import task_suite
from . import training
from . import user_bonus
from . import user_restriction
from . import user_skill
from . import webhook_subscription

from ..__version__ import __version__
from ._converter import structure, unstructure
from .aggregation import AggregatedSolution
from .analytics_request import AnalyticsRequest
from .app import (
    App, AppItem, AppProject, AppBatch, AppBatchPatch, AppBatchCreateRequest,
    AppItemsCreateRequest,
)
from .assignment import Assignment, AssignmentPatch, GetAssignmentsTsvParameters
from .attachment import Attachment
from .clone_results import CloneResults
from .exceptions import (
    IncorrectActionsApiError, raise_on_api_error, ValidationApiError, InternalApiError, TooManyRequestsApiError,
    RemoteServiceUnavailableApiError,
)
from .message_thread import (
    Folder, MessageThread, MessageThreadReply, MessageThreadFolders, MessageThreadCompose
)
from .operation_log import OperationLogItem
from .pool import Pool, PoolPatchRequest
from .primitives.retry import TolokaRetry, SyncRetryingOverURLLibRetry, STATUSES_TO_RETRY
from .primitives.base import autocast_to_enum
from .primitives.parameter import IdempotentOperationParameters
from .project import Project
from .training import Training
from .requester import Requester
from .skill import Skill
from .task import Task
from .task_suite import TaskSuite
from .user_bonus import UserBonus
from .user_restriction import UserRestriction
from .user_skill import SetUserSkillRequest, UserSkill
from .user import User
from ..util import identity
from ..util._managing_headers import add_headers, form_additional_headers, top_level_method_var
from ..util._codegen import expand
from .webhook_subscription import WebhookSubscription

logger = logging.getLogger(__name__)


class TolokaClient:
    """Class that implements interaction with [Toloka API](https://toloka.ai/docs/api/api-reference/).

    Objects of other classes are created and modified only in memory of your computer.
    You can transfer information about these objects to Toloka only by calling one of the `TolokaClient` methods.

    For example, creating an instance of `Project` class will not add a project to Toloka right away. It will create a `Project` instance in your local memory.
    You need to call the `TolokaClient.create_project` method and pass the created project instance to it.
    Likewise, if you read a project using the `TolokaClient.get_project` method, you will get an instance of `Project` class.
    But if you change some parameters in this object manually in your code, it will not affect the existing project in Toloka.
    Call `TolokaClient.update_project` and pass the `Project` to apply your changes.

    Args:
        token: Your OAuth token for Toloka. You can learn more about how to get it [here](https://toloka.ai/docs/api/api-reference/#overview--accessing-the-api)
        environment: There are two environments in Toloka:
            * `SANDBOX` – [Testing environment](https://sandbox.toloka.dev) for Toloka requesters.
            You can test complex projects before assigning tasks to Tolokers. Nobody will see your tasks, and it's free.
            * `PRODUCTION` – [Production environment](https://toloka.dev) for Toloka requesters.
            You spend money there and get the results.

            You need to register in each environment separately. OAuth tokens are generated in each environment separately too.
            Default value: `None`.
        retries: Retry policy for failed API requests.
            Possible values:
            * `int` – The number of retries for all requests. In this case, the retry policy is created automatically.
            * `Retry` object – Deprecated type. Use `retryer_factory` parameter instead.

            Default value: `3`.
        timeout: Number of seconds that [Requests library](https://docs.python-requests.org/en/master) will wait for your client to establish connection to a remote machine.
            Possible values:
            * `float` – Single value for both connect and read timeouts.
            * `Tuple[float, float]` – Tuple sets the values for connect and read timeouts separately.
            * `None` – Set the timeout to `None` only if you are willing to wait the [Response](https://docs.python-requests.org/en/master/api/#requests.Response)
            for unlimited number of seconds.

            Default value: `10.0`.
        url: Set a specific URL instead of Toloka environment. May be useful for testing purposes.
            You can only set one parameter – either `url` or `environment`, not both of them.
            Default value: `None`.
        retry_quotas: List of quotas that must be retried.
            Set `None` or pass an empty list for not retrying any quotas. If you specified the `retries` as `Retry` instance, you must set this parameter to `None`.
            Possible values:
            * `MIN` - Retry minutes quotas.
            * `HOUR` - Retry hourly quotas. This means that the program just sleeps for an hour.
            * `DAY` - Retry daily quotas. We do not recommend retrying these quotas.

            Default value: `MIN`.
        retryer_factory: Factory that creates `Retry` object.
            Fully specified retry policy that will apply to all requests.
            Default value: `None`.
        act_under_account_id: ID of the requester that has been shared access with the current token owner account.
            All requests will be made using a specified account. See [Shared access to the requester's account](https://toloka.ai/docs/guide/multiple-access)
            documentation page. ID of the requester can be retrieved using the [get_requester](toloka.client.TolokaClient.get_requester.md)
            method (this method should be called by the account owner using account's token).
        verify: SSL certificates (a.k.a CA bundle) used to
            verify the identity of requested hosts. Either `True` (default CA bundle),
            a path to an SSL certificate file, an `ssl.SSLContext`, or `False`
            (which will disable verification)

    Example:
        How to create `TolokaClient` instance and make your first request to Toloka.

        >>> your_oauth_token = input('Enter your token:')
        >>> toloka_client = toloka.TolokaClient(your_oauth_token, 'PRODUCTION')  # Or switch to 'SANDBOX' environment
        ...

        {% note info %}

        `toloka_client` instance will be used to pass all API calls later on.

        {% endnote %}
    """

    @unique
    class Environment(Enum):
        SANDBOX = 'https://sandbox.toloka.dev'
        PRODUCTION = 'https://toloka.dev'

        @property
        def platform_url(self):
            if self is TolokaClient.Environment.PRODUCTION:
                return 'https://platform.toloka.ai'
            if self is TolokaClient.Environment.SANDBOX:
                return 'https://sandbox.toloka.yandex.com'

    EXCEPTIONS_TO_RETRY: ClassVar[Tuple[Exception]] = (
        InternalApiError, TooManyRequestsApiError, RemoteServiceUnavailableApiError, HTTPStatusError,
    )

    token: str
    default_timeout: Union[float, Tuple[float, float]]
    _platform_url: Optional[str]
    url: Optional[str]
    retryer_factory: Optional[Callable[[], Retry]]

    def __init__(
        self,
        token: str,
        environment: Union[Environment, str, None] = None,
        retries: Union[int, Retry] = 3,
        timeout: Union[float, Tuple[float, float]] = 10.0,
        url: Optional[str] = None,
        retry_quotas: Union[List[str], str, None] = TolokaRetry.Unit.MIN,
        retryer_factory: Optional[Callable[[], Retry]] = None,
        act_under_account_id: Optional[str] = None,
        verify: VerifyTypes = True,
    ):
        if url is None and environment is None:
            raise ValueError('You must pass at least one parameter: url or environment.')
        if url is not None and environment is not None:
            raise ValueError('You can only pass one parameter: environment or url. Both are now set.')
        if url is not None:
            self.url = url[:-1] if url.endswith('/') else url
            self._platform_url = self.url
        else:
            if not isinstance(environment, TolokaClient.Environment):
                environment = TolokaClient.Environment[environment.upper()]
            self.url = environment.value
            self._platform_url = environment.platform_url
        if isinstance(retries, Retry) and retry_quotas is not None:
            raise ValueError('You must set retry_quotas parameter to None when you specify retries parameters not as int.')
        self.token = token
        # float, or a (connect timeout, read timeout) tuple
        # How long to wait for the server to send data before giving up,
        # If None - wait forever for a response/
        self.default_timeout = timeout

        if isinstance(retries, Retry):
            logger.warning("Retry instance usage isn't thread-safe and is deprecated. Use retryer_factory instead.")
            self.retryer_factory = functools.partial(identity, retries)
        elif retryer_factory:
            self.retryer_factory = retryer_factory
        else:
            self.retryer_factory = functools.partial(self._default_retryer_factory, retries, retry_quotas)

        self.act_under_account_id = act_under_account_id
        self.verify = verify

        self.retrying = SyncRetryingOverURLLibRetry(
            base_url=str(self._session.base_url), retry=self.retryer_factory(), reraise=True,
            exception_to_retry=self.EXCEPTIONS_TO_RETRY,
        )

    @staticmethod
    def _default_retryer_factory(
        retries: int,
        retry_quotas: Union[List[str], str, None],
        status_list: Optional[Sequence[int]] = None,
    ) -> Retry:
        return TolokaRetry(
            retry_quotas=retry_quotas,
            total=retries,
            status_forcelist=list(status_list or STATUSES_TO_RETRY),
            allowed_methods=['HEAD', 'GET', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'POST', 'PATCH'],
            backoff_factor=2,  # summary retry time more than 10 seconds
        )

    def __is_apikey(self) -> bool:
        if self.token.count('.') != 2:
            return False
        dot_pos = self.token.find('.')
        return 21 < dot_pos < 25

    @property
    def _headers(self):
        headers = {
            'Authorization': f'ApiKey {self.token}' if self.__is_apikey() else f'OAuth {self.token}',
            'User-Agent': f'python-toloka-client-{__version__}',
        }
        if self.act_under_account_id:
            headers['X-Act-Under-Account-ID'] = self.act_under_account_id
        return headers

    def _do_request_with_retries(self, method, path, **kwargs):
        @self.retrying.wraps
        def wrapped(method, url, **kwargs):
            response = self._session.request(method, url, **kwargs)
            raise_on_api_error(response)
            return response

        return wrapped(method, path, **kwargs)

    @property
    def _session(self):
        return self._session_for_thread(threading.current_thread().ident)

    @functools.lru_cache(maxsize=128)
    def _session_for_thread(self, thread_id: int) -> httpx.Client:
        client = httpx.Client(headers=self._headers, base_url=self.url, verify=self.verify)
        return client

    def _prepare_request(self, kwargs):
        prepared_kwargs = dict(**kwargs)
        # Fixing capitalisation in boolean parameters
        if prepared_kwargs.get('params'):
            params = prepared_kwargs['params']
            for key, value in params.items():
                if isinstance(value, bool):
                    params[key] = 'true' if value else 'false'
        if self.default_timeout is not None and 'timeout' not in prepared_kwargs:
            prepared_kwargs['timeout'] = self.default_timeout
        # Add additional headers from contextvars
        additional_headers = form_additional_headers()
        headers = prepared_kwargs.get('headers', {})
        headers = {**headers, **additional_headers}
        prepared_kwargs['headers'] = headers
        json_param = prepared_kwargs.pop('json', None)
        if json_param:
            prepared_kwargs['content'] = simplejson.dumps(json_param)
            headers['Content-Type'] = 'application/json'
        return prepared_kwargs

    def _raw_request(self, method, path, **kwargs):
        kwargs = self._prepare_request(kwargs)
        response = self._do_request_with_retries(method, f'/api{path}', **kwargs)
        return response

    def _request(self, method, path, **kwargs):
        return self._raw_request(method, path, **kwargs).json(parse_float=Decimal)

    def _search_request(self, method, path, request, sort, limit):
        params = unstructure(request) or {}
        if sort is not None:
            params['sort'] = unstructure(sort)
        if limit:
            params['limit'] = limit
        return self._request(method, path, params=params)

    def _find_all(self, find_function, request, sort_field: str = 'id', items_field: str = 'items', batch_size: Optional[int] = None):
        result = find_function(request, sort=[sort_field], limit=batch_size)
        items = getattr(result, items_field)
        while result.has_more:
            request = attr.evolve(request, **{f'{sort_field}_gt': getattr(items[-1], sort_field)})
            yield from items
            result = find_function(request, sort=[sort_field], limit=batch_size)
            items = getattr(result, items_field)

        yield from items

    def _async_create_objects_idempotent(
        self,
        url,
        objects,
        parameters,
        operation_type,
    ):
        try:
            response = self._request('post', url, json=unstructure(objects), params=unstructure(parameters))
            insert_operation = structure(response, operation_type)
        except IncorrectActionsApiError as exc:
            if exc.code != 'OPERATION_ALREADY_EXISTS':
                raise

            insert_operation = self.get_operation(operation_id=str(parameters.operation_id))
            if not isinstance(insert_operation, operation_type):
                raise
            insert_operation.raise_on_fail()
            logger.info(f'Objects were not created by {top_level_method_var.get()}: '
                        f'operation {parameters.operation_id} is already submitted.')
        return insert_operation

    def _start_sync_via_async(
        self,
        objects,
        parameters: IdempotentOperationParameters,
        url: str,
        operation_type: operations.Operation,
    ):
        # Index objects to restore sequence in the future
        is_single = not isinstance(objects, list)
        if is_single:
            objects._unexpected['__item_idx'] = '0'
        else:
            for item_idx, obj in enumerate(objects):
                obj._unexpected['__item_idx'] = str(item_idx)

        insert_operation = self._async_create_objects_idempotent(url, objects, parameters, operation_type)
        insert_operation = self.wait_operation(insert_operation, datetime.timedelta(minutes=60))
        return insert_operation

    def _sync_via_async_pool_related(
            self,
            objects,
            parameters: IdempotentOperationParameters,
            url: str,
            result_type,
            operation_type: operations.Operation,
            output_id_field: str,
            get_method: Callable,
    ):
        if not parameters.async_mode:
            response = self._request('post', url, json=unstructure(objects), params=unstructure(parameters))
            return structure(response, result_type)
        is_single = not isinstance(objects, list)
        insert_operation = self._start_sync_via_async(objects, parameters, url, operation_type)

        pools = {}
        validation_errors = {}
        for log_item in self.get_operation_log(insert_operation.id):
            if '__item_idx' in log_item.input:
                index = log_item.input['__item_idx']
            else:
                continue  # operation could be not just creating objects (e.g. open_pool while creating_object)
            if log_item.success:
                numerated_ids = pools.setdefault(log_item.input['pool_id'], {})
                numerated_ids[log_item.output[output_id_field]] = index
            else:
                validation_errors[index] = structure(log_item.output, Dict[str, FieldValidationError])

        # Like in sync methods Exception will raise
        # even if the skip_invalid_items=True but no objects are created
        if validation_errors and not pools:
            raise ValidationApiError(
                code='VALIDATION_ERROR',
                message='Validation failed',
                payload=validation_errors,
            )

        if is_single:
            pool_id = list(pools.keys())[0]
            item_id = list(pools[pool_id].keys())[0]
            return get_method(item_id)
        else:
            items = self._collect_from_pools(get_method, pools)
            return result_type(items=items, validation_errors=validation_errors)

    def _collect_from_pools(self, get_method, pools):
        items = {}
        for pool_id, numerated_ids in pools.items():
            obj_it = get_method(
                pool_id=pool_id,
                id_gte=min(numerated_ids.keys()),
                id_lte=max(numerated_ids.keys()),
            )
            for obj in obj_it:
                if obj.id in numerated_ids:
                    items[numerated_ids[obj.id]] = obj
        return items

    def _sync_via_async(
            self,
            objects: List,
            parameters: IdempotentOperationParameters,
            url: str,
            result_type,
            operation_type: operations.Operation,
            output_id_field: str,
            get_method: Callable,
    ):
        if not parameters.async_mode:
            response = self._request('post', url, json=unstructure(objects), params=unstructure(parameters))
            return structure(response, result_type)
        is_single = not isinstance(objects, list)
        insert_operation = self._start_sync_via_async(objects, parameters, url, operation_type)

        item_id_to_idx = {}
        validation_errors = {}
        for log_item in self.get_operation_log(insert_operation.id):
            if '__item_idx' in log_item.input:
                index = log_item.input['__item_idx']
            else:
                continue  # operation could be not just creating objects (e.g. open_pool while creating_object)
            if log_item.success:
                item_id_to_idx[log_item.output[output_id_field]] = index
            else:
                validation_errors[index] = log_item.output

        # Like as in sync methods Exception will raise
        # even if the skip_invalid_items=True but no objects are created
        if validation_errors and not item_id_to_idx:
            raise ValidationApiError(
                code='VALIDATION_ERROR',
                message='Validation failed',
                payload=validation_errors,
            )

        if is_single:
            item_id = list(item_id_to_idx.keys())[0]
            return get_method(item_id)
        else:
            items = {}
            obj_it = get_method(
                id_gte=min(item_id_to_idx.keys()),
                id_lte=max(item_id_to_idx.keys()),
            )
            for obj in obj_it:
                if obj.id in item_id_to_idx:
                    items[item_id_to_idx[obj.id]] = obj
            return result_type(items=items, validation_errors=validation_errors)

    # Aggregation section

    @expand('request')
    @add_headers('client')
    def aggregate_solutions_by_pool(
        self,
        request: aggregation.PoolAggregatedSolutionRequest,
    ) -> operations.AggregatedSolutionOperation:
        """Starts aggregation of responses in all completed tasks in a pool.

        The method starts the aggregation process on the Toloka server. To wait for the completion of the operation use the [wait_operation](toloka.client.TolokaClient.wait_operation.md) method.

        {% note tip %}

        Try [crowd-kit library](https://toloka.ai/docs/crowd-kit). It has many aggregation methods and executes on your computer.

        {% endnote %}

        Args:
            request: Parameters describing in which pool to aggregate responses and by what rules.

        Returns:
            operations.AggregatedSolutionOperation: An object to track the progress of the operation.

        Example:
            The example shows how to aggregate responses in a pool.

            >>> aggregation_operation = toloka_client.aggregate_solutions_by_pool(
            >>>         type=toloka.client.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
            >>>         pool_id=some_existing_pool_id,
            >>>         answer_weight_skill_id=some_skill_id,
            >>>         fields=[toloka.client.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]
            >>>     )
            >>> aggregation_operation = toloka_client.wait_operation(aggregation_operation)
            >>> aggregation_results = list(toloka_client.get_aggregated_solutions(aggregation_operation.id))
            ...
        """
        data = unstructure(request)
        response = self._request('post', '/v1/aggregated-solutions/aggregate-by-pool', json=data)
        return structure(response, operations.AggregatedSolutionOperation)

    @expand('request')
    @add_headers('client')
    def aggregate_solutions_by_task(self, request: aggregation.WeightedDynamicOverlapTaskAggregatedSolutionRequest) -> AggregatedSolution:
        """Aggregates responses to a single task on the Toloka server.

        {% note tip %}

        Try [crowd-kit library](https://toloka.ai/docs/crowd-kit). It has many aggregation methods and executes on your computer.

        {% endnote %}

        Args:
            request: Aggregation parameters.

        Returns:
            AggregatedSolution: Aggregated response.

        Example:
            The example shows how to aggregate responses to a single task.

            >>> aggregated_response = toloka_client.aggregate_solutions_by_task(
            >>>     pool_id=some_existing_pool_id,
            >>>     task_id=some_existing_task_id,
            >>>     answer_weight_skill_id=some_skill_id,
            >>>     fields=[toloka.client.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]
            >>> )
            >>> print(aggregated_response.output_values['result'])
            ...
        """
        response = self._request('post', '/v1/aggregated-solutions/aggregate-by-task', json=unstructure(request))
        return structure(response, AggregatedSolution)

    @expand('request')
    @add_headers('client')
    def find_aggregated_solutions(self, operation_id: str, request: search_requests.AggregatedSolutionSearchRequest,
                                  sort: Union[List[str], search_requests.AggregatedSolutionSortItems, None] = None,
                                  limit: Optional[int] = None) -> search_results.AggregatedSolutionSearchResult:
        """Finds aggregated responses that match certain criteria.

        Pass to the `find_aggregated_solutions` the ID of the operation started by the [aggregate_solutions_by_pool](toloka.client.TolokaClient.aggregate_solutions_by_pool.md) method.

        The number of returned aggregated responses is limited. To find remaining responses call `find_aggregated_solutions` with updated search criteria.

        To iterate over all matching aggregated responses you may use the [get_aggregated_solutions](toloka.client.TolokaClient.get_aggregated_solutions.md) method.

        Args:
            operation_id: The ID of the aggregation operation.
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned aggregated responses limit. The default limit is 50. The maximum allowed limit is 100,000.

        Returns:
            AggregatedSolutionSearchResult: Found responses and a flag showing whether there are more matching responses exceeding the limit.

        Example:
            The example shows how to get all aggregated responses using the `find_aggregated_solutions` method.

            >>> # run toloka_client.aggregate_solutions_by_pool and wait for the operation to complete.
            >>> current_result = toloka_client.find_aggregated_solutions(aggregation_operation.id)
            >>> aggregation_results = current_result.items
            >>> # If we have more results, let's get them
            >>> while current_result.has_more:
            >>>     current_result = toloka_client.find_aggregated_solutions(
            >>>         aggregation_operation.id,
            >>>         task_id_gt=current_result.items[-1].task_id,
            >>>     )
            >>>     aggregation_results = aggregation_results + current_result.items
            >>> print(len(aggregation_results))
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.AggregatedSolutionSortItems)
        response = self._search_request('get', f'/v1/aggregated-solutions/{operation_id}', request, sort, limit)
        return structure(response, search_results.AggregatedSolutionSearchResult)

    @expand('request')
    @add_headers('client')
    def get_aggregated_solutions(
        self,
        operation_id: str, request: search_requests.AggregatedSolutionSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[AggregatedSolution, None, None]:
        """Finds all aggregated responses that match certain criteria.

        Pass to the `get_aggregated_solutions` the ID of the operation started by the [aggregate_solutions_by_pool](toloka.client.TolokaClient.aggregate_solutions_by_pool.md) method.

        `get_aggregated_solutions` returns a generator. You can iterate over all found aggregated responses using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort aggregated responses use the [find_aggregated_solutions](toloka.client.TolokaClient.find_aggregated_solutions.md) method.

        {% note tip %}

        Try [crowd-kit library](https://toloka.ai/docs/crowd-kit). It has many aggregation methods and executes on your computer.

        {% endnote %}

        Args:
            operation_id: The ID of the aggregation operation.
            request: Search criteria.
            batch_size: Returned aggregated responses limit for each request. The default batch_size is 50. The maximum allowed limit is 100,000.

        Yields:
            AggregatedSolution: The next matching aggregated response.

        Example:
            The example shows how to aggregate responses in a pool.

            >>> aggregation_operation = toloka_client.aggregate_solutions_by_pool(
            >>>     type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
            >>>     pool_id=some_existing_pool_id,
            >>>     answer_weight_skill_id=some_skill_id,
            >>>     fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]
            >>> )
            >>> aggregation_operation = toloka_client.wait_operation(aggregation_operation)
            >>> aggregation_results = list(toloka_client.get_aggregated_solutions(aggregation_operation.id))
            ...
        """
        find_function = functools.partial(self.find_aggregated_solutions, operation_id)
        generator = self._find_all(find_function, request, sort_field='task_id', batch_size=batch_size)
        yield from generator

    # Assignments section

    @add_headers('client')
    def accept_assignment(self, assignment_id: str, public_comment: str) -> Assignment:
        """Accepts an assignment.

        Args:
            assignment_id: The ID of the assignment.
            public_comment: A comment visible to Tolokers.

        Returns:
            Assignment: The assignment object with the updated status field.

        Example:
            Accepting an assignment.

            >>> toloka_client.accept_assignment(assignment_id, 'Well done!')
            ...
        """
        return self.patch_assignment(assignment_id, public_comment=public_comment, status=Assignment.ACCEPTED)

    @expand('request')
    @add_headers('client')
    def find_assignments(self, request: search_requests.AssignmentSearchRequest,
                         sort: Union[List[str], search_requests.AssignmentSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.AssignmentSearchResult:
        """Finds assignments that match certain criteria.

        The number of returned assignments is limited. To find remaining assignments call `find_assignments` with updated search criteria.

        To iterate over all matching assignments you may use the [get_assignments](toloka.client.TolokaClient.get_assignments.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned assignments limit. The default limit is 50. The maximum allowed limit is 100,000.

        Returns:
            AssignmentSearchResult: Found assignments and a flag showing whether there are more matching assignments.

        Example:
            Search for `SKIPPED` or `EXPIRED` assignments in the specified pool.

            >>> toloka_client.find_assignments(pool_id='1', status = ['SKIPPED', 'EXPIRED'])
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.AssignmentSortItems)
        response = self._search_request('get', '/v1/assignments', request, sort, limit)
        return structure(response, search_results.AssignmentSearchResult)

    @add_headers('client')
    def get_assignment(self, assignment_id: str) -> Assignment:
        """Gets an assignment from Toloka.

        Args:
            assignment_id: The ID of the assignment.

        Returns:
            Assignment: The assignment.

        Example:
            >>> toloka_client.get_assignment(assignment_id='1')
            ...
        """
        response = self._request('get', f'/v1/assignments/{assignment_id}')
        return structure(response, Assignment)

    @expand('request')
    @add_headers('client')
    def get_assignments(
        self,
        request: search_requests.AssignmentSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[Assignment, None, None]:
        """Finds all assignments that match certain criteria.

        `get_assignments` returns a generator. You can iterate over all found assignments using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort assignments use the [find_assignments](toloka.client.TolokaClient.find_assignments.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned assignments limit for each request. The default batch_size  is 50. The maximum allowed batch_size  is 100,000.

        Yields:
            Assignment: The next matching assignment.

        Example:
            The following example creates the list with IDs of `SUBMITTED` assignments in the specified pool.

            >>> from toloka.client import Assignment
            >>> assignments = toloka_client.get_assignments(pool_id='1', status=Assignment.SUBMITTED)
            >>> result_list = [assignment.id for assignment in assignments]
            ...
        """
        generator = self._find_all(self.find_assignments, request, batch_size=batch_size)
        yield from generator

    @expand('patch')
    @add_headers('client')
    def patch_assignment(self, assignment_id: str, patch: AssignmentPatch) -> Assignment:
        """Changes an assignment status and associated public comment.

        See also [reject_assignment](toloka.client.TolokaClient.reject_assignment.md) and [accept_assignment](toloka.client.TolokaClient.accept_assignment.md).

        Args:
            assignment_id: The ID of the assignment.
            patch: New status and comment.

        Returns:
            Assignment: Assignment object with updated fields.

        Example:
            >>> toloka_client.patch_assignment(assignment_id='1', public_comment='Accepted. Good job.', status='ACCEPTED')
            ...
        """
        response = self._request('patch', f'/v1/assignments/{assignment_id}', json=unstructure(patch))
        return structure(response, Assignment)

    @add_headers('client')
    def reject_assignment(self, assignment_id: str, public_comment: str) -> Assignment:
        """Rejects an assignment.

        Args:
            assignment_id: The ID of the assignment.
            public_comment: A public comment visible to Tolokers.

        Returns:
            Assignment: Assignment object with updated fields.

        Example:
            >>> toloka_client.reject_assignment(assignment_id='1', 'Some questions skipped')
            ...
        """
        return self.patch_assignment(assignment_id, public_comment=public_comment, status=Assignment.REJECTED)

    # Attachment section

    @expand('request')
    @add_headers('client')
    def find_attachments(self, request: search_requests.AttachmentSearchRequest,
                         sort: Union[List[str], search_requests.AttachmentSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.AttachmentSearchResult:
        """Finds attachments that match certain criteria and returns their metadata.

        The number of returned attachments is limited. To find remaining attachments call `find_attachments` with updated search criteria.

        To iterate over all matching attachments you may use the [get_attachments](toloka.client.TolokaClient.get_attachments.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned attachments limit. The maximum allowed limit is 100.

        Returns:
            AttachmentSearchResult: Found attachments and a flag showing whether there are more matching attachments exceeding the limit.

        Example:
            Let's find attachments in the pool and sort them by the ID and the date of creation in descending order.

            >>> attachments = toloka_client.find_attachments(pool_id='1', sort=['-created', '-id'], limit=10)
            ...

            If there are attachments exceeding the `limit`, then `attachments.has_more` is set to `True`.
        """
        sort = None if sort is None else structure(sort, search_requests.AttachmentSortItems)
        response = self._search_request('get', '/v1/attachments', request, sort, limit)
        return structure(response, search_results.AttachmentSearchResult)

    @add_headers('client')
    def get_attachment(self, attachment_id: str) -> Attachment:
        """Gets attachment metadata without downloading it

        To download attachments as a file use "TolokaClient.download_attachment" method.

        Args:
            attachment_id: ID of attachment.

        Returns:
            Attachment: The attachment metadata read as a result.

        Example:
            Specify an `attachment_id` to get the information about any attachment object.

            >>> toloka_client.get_attachment(attachment_id='1')
            ...
        """
        response = self._request('get', f'/v1/attachments/{attachment_id}')
        return structure(response, Attachment)

    @expand('request')
    @add_headers('client')
    def get_attachments(
        self,
        request: search_requests.AttachmentSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[Attachment, None, None]:
        """Finds all attachments that match certain criteria and returns their metadata.

        `get_attachments` returns a generator. You can iterate over all found attachments using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort attachments use the [find_attachments](toloka.client.TolokaClient.find_attachments.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned attachments limit for each request. The maximum allowed batch_size is 100.

        Yields:
            Attachment: The next matching attachment.

        Example:
            Make a list of all received attachments in the specified pool.

            >>> results_list = list(toloka_client.get_attachments(pool_id='1'))
            ...
        """
        generator = self._find_all(self.find_attachments, request, batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def download_attachment(self, attachment_id: str, out: BinaryIO) -> None:
        """Downloads specific attachment

        Args:
            attachment_id: ID of attachment.
            out: File object where to put downloaded file.

        Example:
            How to download an attachment.

            >>> with open('my_new_file.txt', 'wb') as out_f:
            >>>     toloka_client.download_attachment(attachment_id='1', out=out_f)
            ...
        """
        response = self._raw_request('get', f'/v1/attachments/{attachment_id}/download')
        out.write(response.content)

    # Message section

    @autocast_to_enum
    @add_headers('client')
    def add_message_thread_to_folders(
        self,
        message_thread_id: str, folders: Union[List[Folder], MessageThreadFolders]
    ) -> MessageThread:
        """Adds a message thread to folders.

        Args:
            message_thread_id: The ID of the message thread.
            folders: A list of folders where to add the thread.

        Returns:
            MessageThread: The updated message thread.

        Example:
            >>> toloka_client.add_message_thread_to_folders(message_thread_id='1', folders=['IMPORTANT'])
            ...
        """
        if not isinstance(folders, MessageThreadFolders):
            folders = structure({'folders': folders}, MessageThreadFolders)
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/add-to-folders', json=unstructure(folders))
        return structure(response, MessageThread)

    @expand('compose')
    @add_headers('client')
    def compose_message_thread(self, compose: MessageThreadCompose) -> MessageThread:
        """Creates a message thread and sends the first thread message to Tolokers.

        Args:
            compose: Parameters for creating the message thread.

        Returns:
            MessageThread: The created message thread.

        Example:
            A message is sent to all Tolokers who have tried to complete your tasks.
            The message is in english. Tolokers can't reply to your message.

            >>> message_text = "Amazing job! We've just trained our first model with the data you prepared for us. Thank you!"
            >>> toloka_client.compose_message_thread(
            >>>     recipients_select_type='ALL',
            >>>     topic={'EN': 'Thank you!'},
            >>>     text={'EN': message_text},
            >>>     answerable=False
            >>> )
            ...
        """
        response = self._request('post', '/v1/message-threads/compose', json=unstructure(compose))
        return structure(response, MessageThread)

    @expand('request')
    @add_headers('client')
    def find_message_threads(self, request: search_requests.MessageThreadSearchRequest,
                             sort: Union[List[str], search_requests.MessageThreadSortItems, None] = None,
                             limit: Optional[int] = None) -> search_results.MessageThreadSearchResult:
        """Finds message threads that match certain criteria.

        The number of returned message threads is limited. To find remaining threads call `find_message_threads` with updated search criteria.

        To iterate over all matching threads you may use the [get_message_threads](toloka.client.TolokaClient.get_message_threads.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned message threads limit. The default limit is 50. The maximum allowed limit is 300.

        Returns:
            MessageThreadSearchResult: Found message threads and a flag showing whether there are more matching threads.

        Example:
            Finding all message threads in the `INBOX` folder.

            >>> toloka_client.find_message_threads(folder='INBOX')
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.MessageThreadSortItems)
        response = self._search_request('get', '/v1/message-threads', request, sort, limit)
        return structure(response, search_results.MessageThreadSearchResult)

    @add_headers('client')
    def reply_message_thread(self, message_thread_id: str, reply: MessageThreadReply) -> MessageThread:
        """Sends a reply message in a thread.

        Args:
            message_thread_id: The ID of the thread.
            reply: The reply message.

        Returns:
            MessageThread: The updated message thread.

        Example:
            Sending a reply to all unread messages.

            >>> message_threads = toloka_client.get_message_threads(folder='UNREAD')
            >>> message_reply = {'EN': 'Thank you for your message! I will get back to you soon.'}
            >>> for thread in message_threads:
            >>>     toloka_client.reply_message_thread(
            >>>         message_thread_id=thread.id,
            >>>         reply=toloka.client.message_thread.MessageThreadReply(text=message_reply)
            >>>     )
            ...
        """
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/reply', json=unstructure(reply))
        return structure(response, MessageThread)

    @expand('request')
    @add_headers('client')
    def get_message_threads(
        self,
        request: search_requests.MessageThreadSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[MessageThread, None, None]:
        """Finds all message threads that match certain criteria.

        `get_message_threads` returns a generator. You can iterate over all found message threads using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort message threads use the [find_message_threads](toloka.client.TolokaClient.find_message_threads.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned message threads limit for each request. The default batch_size is 50. The maximum allowed batch_size is 300.

        Yields:
            MessageThread: The next matching message thread.

        Example:
            How to get all unread incoming messages.

            >>> message_threads = toloka_client.get_message_threads(folder=['INBOX', 'UNREAD'])
            ...
        """
        generator = self._find_all(self.find_message_threads, request, batch_size=batch_size)
        yield from generator

    @autocast_to_enum
    @add_headers('client')
    def remove_message_thread_from_folders(self, message_thread_id: str,
                                           folders: Union[List[Folder], MessageThreadFolders]) -> MessageThread:
        """Removes a message thread from folders.

        Args:
            message_thread_id: The ID of the message thread.
            folders: A list of folders.

        Returns:
            MessageThread: The updated message thread.

        Example:
            >>> toloka_client.remove_message_thread_from_folders(message_thread_id='1', folders=['IMPORTANT'])
            ...
        """
        if not isinstance(folders, MessageThreadFolders):
            folders = structure({'folders': folders}, MessageThreadFolders)
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/remove-from-folders', json=unstructure(folders))
        return structure(response, MessageThread)

    # Project section

    @add_headers('client')
    def archive_project(self, project_id: str) -> Project:
        """Archives a project.

        All pools in the project must be archived before archiving the project.

        The archived project is not deleted. You can access it if you need.

        Args:
            project_id: The ID of project to be archived.

        Returns:
            Project: The project with the updated status.

        Example:
            >>> toloka_client.archive_project(project_id='1')
            ...
        """
        operation = self.archive_project_async(project_id)
        operation = self.wait_operation(operation)
        return self.get_project(operation.parameters.project_id)

    @add_headers('client')
    def archive_project_async(self, project_id: str) -> operations.ProjectArchiveOperation:
        """Archives a project. Sends an asynchronous request to Toloka.

        All pools in the project must be archived before archiving the project.

        The archived project is not deleted. You can access it if you need.

        Args:
            project_id: The ID of project to be archived.

        Returns:
            ProjectArchiveOperation: An object to track the progress of the operation.

        Example:
            >>> archive_op = toloka_client.archive_project_async(project_id='1')
            >>> toloka_client.wait_operation(archive_op)
            ...
        """
        response = self._request('post', f'/v1/projects/{project_id}/archive')
        return structure(response, operations.ProjectArchiveOperation)

    @add_headers('client')
    def create_project(self, project: Project) -> Project:
        """Creates a new project in Toloka.

        You can send a maximum of 20 requests of this kind per minute and a maximum of 100 requests per day.

        Args:
            project: The project to be created.

        Returns:
            Project: The project with updated read-only fields.

        Example:
            Creating a new project.

            >>> new_project = toloka.client.project.Project(
            >>>     assignments_issuing_type=toloka.client.project.Project.AssignmentsIssuingType.AUTOMATED,
            >>>     public_name='My best project',
            >>>     public_description='Describe the picture',
            >>>     public_instructions='Describe in a few words what is happening in the image.',
            >>>     task_spec=toloka.client.project.task_spec.TaskSpec(
            >>>         input_spec={'image': toloka.client.project.field_spec.UrlSpec()},
            >>>         output_spec={'result': toloka.client.project.field_spec.StringSpec()},
            >>>         view_spec=project_interface,
            >>>     ),
            >>> )
            >>> new_project = toloka_client.create_project(new_project)
            >>> print(new_project.id)
            ...
        """
        response = self._request('post', '/v1/projects', json=unstructure(project))
        result = structure(response, Project)
        logger.info(f'A new project with ID "{result.id}" has been created. Link to open in web interface: {self._platform_url}/requester/project/{result.id}')
        return result

    @expand('request')
    @add_headers('client')
    def find_projects(self, request: search_requests.ProjectSearchRequest,
                      sort: Union[List[str], search_requests.ProjectSortItems, None] = None,
                      limit: Optional[int] = None) -> search_results.ProjectSearchResult:
        """Finds projects that match certain criteria.

        The number of returned projects is limited. To find remaining projects call `find_projects` with updated search criteria.

        To iterate over all matching projects you may use the [get_projects](toloka.client.TolokaClient.get_projects.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned projects limit. The default limit is 20. The maximum allowed limit is 300.

        Returns:
            ProjectSearchResult: Found projects and a flag showing whether there are more matching projects exceeding the limit.

        Example:
            The example shows how to find projects created before a specific date.

            >>> projects = toloka_client.find_projects(created_lt='2021-06-01T00:00:00')
            ...

            If there are projects exceeding the `limit`, then `projects.has_more` is set to `True`.
        """
        sort = None if sort is None else structure(sort, search_requests.ProjectSortItems)
        response = self._search_request('get', '/v1/projects', request, sort, limit)
        return structure(response, search_results.ProjectSearchResult)

    @add_headers('client')
    def get_project(self, project_id: str) -> Project:
        """Gets project data from Toloka.

        Args:
            project_id: The ID of the project.

        Returns:
            Project: The project.

        Example:
            >>> toloka_client.get_project(project_id='1')
            ...
        """
        response = self._request('get', f'/v1/projects/{project_id}')
        return structure(response, Project)

    @expand('request')
    @add_headers('client')
    def get_projects(
        self,
        request: search_requests.ProjectSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[Project, None, None]:
        """Finds all projects that match certain criteria.

        `get_projects` returns a generator. You can iterate over all found projects using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort projects use the [find_projects](toloka.client.TolokaClient.find_projects.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned projects limit for each request. The default batch_size is 20. The maximum allowed batch_size is 300.

        Yields:
            Project: The next matching project.
        Example:
            Get all active projects.

            >>> active_projects = toloka_client.get_projects(status='ACTIVE')
            ...

            Get all your projects.

            >>> my_projects = toloka_client.get_projects()
            ...
        """
        generator = self._find_all(self.find_projects, request, batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def update_project(self, project_id: str, project: Project) -> Project:
        """Updates all project parameters in Toloka.

        Args:
            project_id: The ID of the project to be updated.
            project: The project with new parameters.

        Returns:
            Project: The project with updated parameters.

        Example:
            >>> updated_project = toloka_client.get_project(project_id='1')
            >>> updated_project.private_comment = 'example project'
            >>> updated_project = toloka_client.update_project(project_id=updated_project.id, project=updated_project)
            ...
        """
        response = self._request('put', f'/v1/projects/{project_id}', json=unstructure(project))
        return structure(response, Project)

    @add_headers('client')
    def clone_project(self, project_id: str, reuse_controllers: bool = True) -> CloneResults:
        """Clones a project and all pools and trainings inside it.

        `clone_project` emulates cloning behavior via Toloka interface. Note that it calls several API methods. If some method fails then the project may be partially cloned.

        Important notes:
        * No tasks are cloned.
        * The expiration date is not changed in the new project.
        * The same skills are used.
        * If `reuse_controllers` is `True`, quality control collectors monitor both projects.
            For example, the `fast_submitted_count` rule counts fast responses in the cloned and new projects together.

        Args:
            project_id: The ID of the project to be cloned.
            reuse_controllers:
                * `True` — Use same quality controllers in cloned and created projects.
                * `False` — Use separate quality controllers.

                Default value: `True`.

        Returns:
            Tuple[Project, List[Pool], List[Training]]: Created project, pools and trainings.

        Example:

            >>> project, pools, trainings = toloka_client.clone_project('123')
            >>> # add tasks in pools and trainings
            ...
        """

        def reset_quality_control(quality_control, old_to_new_train_ids):
            if quality_control is None:
                return
            if not reuse_controllers:
                for quality_control_config in quality_control.configs:
                    quality_control_config.collector_config.uuid = None
            if (
                hasattr(quality_control, 'training_requirement') and
                hasattr(quality_control.training_requirement, 'training_pool_id') and
                quality_control.training_requirement.training_pool_id is not None
            ):
                new_id = old_to_new_train_ids[quality_control.training_requirement.training_pool_id]
                quality_control.training_requirement.training_pool_id = new_id

        # clone project
        project_for_clone = self.get_project(project_id)
        project_quality_control = project_for_clone.quality_control
        project_for_clone.quality_control = None
        new_project = self.create_project(project_for_clone)

        # create trainings
        new_trainings = []
        old_to_new_train_ids = {}
        for training in self.get_trainings(project_id=project_id):  # noqa
            old_id = training.id
            training.project_id = new_project.id
            new_training = self.create_training(training)
            new_trainings.append(new_training)
            old_to_new_train_ids[old_id] = new_training.id

        # save quality control on project
        reset_quality_control(project_quality_control, old_to_new_train_ids)
        if project_quality_control is not None:
            new_project.quality_control = project_quality_control
            new_project = self.update_project(new_project.id, new_project)

        # create new pools
        new_pools = []
        for pool in self.get_pools(project_id=project_id):
            pool.project_id = new_project.id
            reset_quality_control(pool.quality_control, old_to_new_train_ids)
            new_pools.append(self.create_pool(pool))

        return CloneResults(project=new_project, pools=new_pools, trainings=new_trainings)

    # Pool section

    @add_headers('client')
    def archive_pool(self, pool_id: str) -> Pool:
        """Archives a pool.

        Only closed pools can be archived.

        You can't open archived pools, but you can [clone](toloka.client.TolokaClient.clone_pool.md) them if needed.

        Args:
            pool_id: The ID of the pool to be archived.

        Returns:
            Pool: The pool with updated status.

        Example:
            >>> closed_pool = next(toloka_client.get_pools(status='CLOSED'))
            >>> toloka_client.archive_pool(pool_id=closed_pool.id)
            ...
        """
        operation = self.archive_pool_async(pool_id)
        if operation:
            operation = self.wait_operation(operation)
            operation.raise_on_fail()
        return self.get_pool(pool_id)

    @add_headers('client')
    def archive_pool_async(self, pool_id: str) -> Optional[operations.PoolArchiveOperation]:
        """Archives a pool. Sends an asynchronous request to Toloka.

        Only closed pools can be archived.

        You can't open archived pools, but you can [clone](toloka.client.TolokaClient.clone_pool.md) them if needed.

        Args:
            pool_id: The ID of the pool to be archived.

        Returns:
            PoolArchiveOperation: An object to track the progress of the operation. If the pool is already archived then `None` is returned.

        Example:
            >>> closed_pool = next(toloka_client.get_pools(status='CLOSED'))
            >>> archive_op = toloka_client.archive_pool_async(pool_id=closed_pool.id)
            >>> toloka_client.wait_operation(archive_op)
            ...
        """
        response = self._raw_request('post', f'/v1/pools/{pool_id}/archive')
        # is pool already archived?
        if response.status_code == 204:
            return
        return structure(response.json(), operations.PoolArchiveOperation)

    @add_headers('client')
    def close_pool(self, pool_id: str) -> Pool:
        """Closes a pool.

        If all tasks in a pool are completed, then the pool is closed automatically.

        Args:
            pool_id: The ID of the pool to be closed.

        Returns:
            Pool: The pool with updated status.

        Example:
            >>> open_pool = next(toloka_client.get_pools(status='OPEN'))
            >>> toloka_client.close_pool(pool_id=open_pool.id)
            ...
        """
        operation = self.close_pool_async(pool_id)
        if operation:
            operation = self.wait_operation(operation)
            operation.raise_on_fail()

        return self.get_pool(pool_id)

    @add_headers('client')
    def close_pool_async(self, pool_id: str) -> Optional[operations.PoolCloseOperation]:
        """Closes a pool. Sends an asynchronous request to Toloka.

        If all tasks in a pool are completed, then the pool is closed automatically.

        Args:
            pool_id: The ID of the pool to be closed.

        Returns:
            PoolCloseOperation: An object to track the progress of the operation. If the pool is already closed then `None` is returned.

        Example:
            >>> open_pool = next(toloka_client.get_pools(status='OPEN'))
            >>> close_op = toloka_client.close_pool_async(pool_id=open_pool.id)
            >>> toloka_client.wait_operation(close_op)
            ...
        """
        response = self._raw_request('post', f'/v1/pools/{pool_id}/close')
        # is pool already closed?
        if response.status_code == 204:
            return None
        return structure(response.json(), operations.PoolCloseOperation)

    @add_headers('client')
    def close_pool_for_update(self, pool_id: str) -> Pool:
        """Closes a pool that is to be updated.

        To make changes to a pool, close it before updating parameters.
        If you don't open the pool after updating, it opens automatically in 15 minutes.

        Args:
            pool_id: The ID of the pool to be closed.

        Returns:
            Pool: The pool with updated status.

        Example:
            >>> toloka_client.close_pool_for_update(pool_id='1')
            ...
        """
        operation = self.close_pool_for_update_async(pool_id)
        if operation:
            operation = self.wait_operation(operation)
            operation.raise_on_fail()
        return self.get_pool(pool_id)

    @add_headers('client')
    def close_pool_for_update_async(self, pool_id: str) -> Optional[operations.PoolCloseOperation]:
        """Closes a pool that is to be updated. Sends an asynchronous request to Toloka.

        To make changes to a pool, close it before updating parameters.
        If you don't open the pool after updating, it opens automatically in 15 minutes.

        Args:
            pool_id: The ID of the pool to be closed.

        Returns:
            PoolCloseOperation: An object to track the progress of the operation. If the pool is already closed then `None` is returned.

        Example:
            >>> close_op = toloka_client.close_pool_for_update_async(pool_id='1')
            >>> toloka_client.wait_operation(close_op)
            ...
        """
        response = self._raw_request('post', f'/v1/pools/{pool_id}/close-for-update')
        # is pool already closed for update?
        if response.status_code == 204:
            return None
        return structure(response.json(), operations.PoolCloseOperation)

    @add_headers('client')
    def clone_pool(self, pool_id: str) -> Pool:
        """Clones an existing pool.

        An empty pool with the same parameters is created.
        The new pool is attached to the same project.

        Args:
            pool_id: The ID of the pool to be cloned.

        Returns:
            Pool: The new pool.

        Example:
            >>> toloka_client.clone_pool(pool_id='1')
            ...
        """
        operation = self.clone_pool_async(pool_id)
        operation = self.wait_operation(operation)
        result = self.get_pool(operation.details.pool_id)
        logger.info(
            f'A new pool with ID "{result.id}" has been cloned. Link to open in web interface: '
            f'{self._platform_url}/requester/project/{result.project_id}/pool/{result.id}'
        )
        return result

    @add_headers('client')
    def clone_pool_async(self, pool_id: str) -> operations.PoolCloneOperation:
        """Clones an existing pool. Sends an asynchronous request to Toloka.

        An empty pool with the same parameters is created.
        The new pool is attached to the same project.

        Args:
            pool_id: The ID of the pool to be cloned.

        Returns:
            PoolCloneOperation: An object to track the progress of the operation.

        Example:
            >>> clone_op = toloka_client.clone_pool_async(pool_id='1')
            >>> toloka_client.wait_operation(clone_op)
            ...
        """
        response = self._request('post', f'/v1/pools/{pool_id}/clone')
        return structure(response, operations.PoolCloneOperation)

    @add_headers('client')
    def create_pool(self, pool: Pool) -> Pool:
        """Creates a new pool in Toloka.

        You can send a maximum of 20 requests of this kind per minute and 100 requests per day.

        Args:
            pool: The pool to be created.

        Returns:
            Pool: The pool with updated read-only fields.

        Example:
            Creating a new pool.

            >>> new_pool = toloka.client.Pool(
            >>>     project_id='1',
            >>>     private_name='Pool 1',
            >>>     may_contain_adult_content=False,
            >>>     will_expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365),
            >>>     reward_per_assignment=0.01,
            >>>     assignment_max_duration_seconds=60*20,
            >>>     defaults=toloka.client.Pool.Defaults(default_overlap_for_new_task_suites=3),
            >>>     filter=toloka.client.filter.Languages.in_('EN'),
            >>> )
            >>> new_pool.set_mixer_config(real_tasks_count=10, golden_tasks_count=0, training_tasks_count=0)
            >>> new_pool.quality_control.add_action(...)
            >>> new_pool = toloka_client.create_pool(new_pool)
            >>> print(new_pool.id)
            ...
        """
        if pool.type == Pool.Type.TRAINING:
            raise ValueError('Training pools are not supported')

        response = self._request('post', '/v1/pools', json=unstructure(pool))
        result = structure(response, Pool)
        logger.info(
            f'A new pool with ID "{result.id}" has been created. Link to open in web interface: '
            f'{self._platform_url}/requester/project/{result.project_id}/pool/{result.id}'
        )
        return result

    @expand('request')
    @add_headers('client')
    def find_pools(self, request: search_requests.PoolSearchRequest,
                   sort: Union[List[str], search_requests.PoolSortItems, None] = None,
                   limit: Optional[int] = None) -> search_results.PoolSearchResult:
        """Finds pools that match certain criteria.

        The number of returned pools is limited. To find remaining pools call `find_pools` with updated search criteria.

        To iterate over all matching pools you may use the [get_pools](toloka.client.TolokaClient.get_pools.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned pools limit. The default limit is 20. The maximum allowed limit is 300.

        Returns:
           PoolSearchResult: Found pools and a flag showing whether there are more matching pools exceeding the limit.

        Examples:
            Finding all pools in all projects.

            >>> pools = toloka_client.find_pools()
            ...

            Finding all open pools in all projects.

            >>> pools = toloka_client.find_pools(status='OPEN')
            ...

            Finding open pools in a specific project.

            >>> pools = toloka_client.find_pools(status='OPEN', project_id='1')
            ...

            If there are pools exceeding the `limit`, then `pools.has_more` is set to `True`.
        """
        sort = None if sort is None else structure(sort, search_requests.PoolSortItems)
        response = self._search_request('get', '/v1/pools', request, sort, limit)
        return structure(response, search_results.PoolSearchResult)

    @add_headers('client')
    def get_pool(self, pool_id: str) -> Pool:
        """Gets pool data from Toloka.

        Args:
            pool_id: The ID of the pool.

        Returns:
            Pool: The pool.

        Example:
            >>> toloka_client.get_pool(pool_id='1')
            ...
        """
        response = self._request('get', f'/v1/pools/{pool_id}')
        return structure(response, Pool)

    @expand('request')
    @add_headers('client')
    def get_pools(
        self,
        request: search_requests.PoolSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[Pool, None, None]:
        """Finds all pools that match certain criteria.

        `get_pools` returns a generator. You can iterate over all found pools using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort pools use the [find_pools](toloka.client.TolokaClient.find_pools.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned pools limit for each request. The default batch_size is 20. The maximum allowed batch_size is 300.

        Yields:
            Pool: The next matching pool.

        Example:
            How to get all open pools from a project.

            >>> open_pools = toloka_client.get_pools(project_id='1', status='OPEN')
            ...

            How to get all pools from a project.

            >>> all_pools = toloka_client.get_pools(project_id='1')
            ...
        """
        generator = self._find_all(self.find_pools, request, batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def open_pool(self, pool_id: str) -> Pool:
        """Opens a pool.

        After opening the pool, tasks can be assigned to Tolokers.

        Args:
            pool_id: The ID of the pool.

        Returns:
            Pool: The pool with updated status.

        Example:
            Opening a pool.

            >>> toloka_client.open_pool(pool_id='1')
            ...
        """
        operation = self.open_pool_async(pool_id)
        if operation:
            operation = self.wait_operation(operation)
            operation.raise_on_fail()

        return self.get_pool(pool_id)

    @add_headers('client')
    def open_pool_async(self, pool_id: str) -> Optional[operations.PoolOpenOperation]:
        """Opens a pool. Sends an asynchronous request to Toloka.

        After opening the pool, tasks can be assigned to Tolokers.

        Args:
            pool_id: The ID of the pool.

        Returns:
            PoolOpenOperation: An object to track the progress of the operation. If the pool is already opened then `None` is returned.

        Example:
            Opening a pool.

            >>> open_op = toloka_client.open_pool(pool_id='1')
            >>> toloka_client.wait_operation(open_op)
            ...
        """
        response = self._raw_request('post', f'/v1/pools/{pool_id}/open')
        # is pool already opened?
        if response.status_code == 204:
            return None
        return structure(response.json(), operations.PoolOpenOperation)

    @expand('request')
    @add_headers('client')
    def patch_pool(self, pool_id: str, request: PoolPatchRequest) -> Pool:
        """Changes pool parameters in Toloka.

        If a parameter is not specified in the `patch_pool` method, then it is left unchanged in Toloka.

        Args:
            pool_id: The ID of the pool to be changed.
            request: New pool parameters.

        Returns:
            Pool: The pool with updated parameters.

        Example:
            Changing priority of a pool.

            >>> toloka_client.patch_pool(pool_id='1', priority=100)
            ...
        """
        response = self._request('patch', f'/v1/pools/{pool_id}', json=unstructure(request))
        return structure(response, Pool)

    @add_headers('client')
    def update_pool(self, pool_id: str, pool: Pool) -> Pool:
        """Updates all pool parameters in Toloka.

        Args:
            pool_id: The ID of the pool to be updated.
            pool: The pool with new parameters.

        Returns:
            Pool: The pool with updated parameters.

        Example:
            >>> updated_pool = toloka_client.get_pool(pool_id='1')
            >>> updated_pool.will_expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
            >>> toloka_client.update_pool(pool_id=updated_pool.id, pool=updated_pool)
            ...
        """
        if pool.type == Pool.Type.TRAINING:
            raise ValueError('Training pools are not supported')
        response = self._request('put', f'/v1/pools/{pool_id}', json=unstructure(pool))
        return structure(response, Pool)

    # Training section

    @add_headers('client')
    def archive_training(self, training_id: str) -> Training:
        """Archives a training.

        Only closed trainings can be archived.

        You can access archived trainings later.

        Args:
            training_id: The ID of the training to be archived.

        Returns:
            Training: The training with updated status.

        Example:
            >>> closed_training = next(toloka_client.get_trainings(status='CLOSED'))
            >>> toloka_client.archive_training(training_id=closed_training.id)
            ...
        """
        operation = self.archive_training_async(training_id)
        if operation:
            operation = self.wait_operation(operation)
            operation.raise_on_fail()
        return self.get_training(training_id)

    @add_headers('client')
    def archive_training_async(self, training_id: str) -> Optional[operations.TrainingArchiveOperation]:
        """Archives a training. Sends an asynchronous request to Toloka.

        Only closed trainings can be archived.

        You can access archived trainings later.

        Args:
            training_id: The ID of the training to be archived.

        Returns:
            TrainingArchiveOperation: An object to track the progress of the operation. If the training is already archived then `None` is returned.

        Example:
            >>> closed_training = next(toloka_client.find_trainings(status='CLOSED'))
            >>> archive_op = toloka_client.archive_training_async(training_id=closed_training.id)
            >>> toloka_client.wait_operation(archive_op)
            ...
        """
        response = self._raw_request('post', f'/v1/trainings/{training_id}/archive')
        # is training already archived?
        if response.status_code == 204:
            return
        return structure(response.json(), operations.TrainingArchiveOperation)

    @add_headers('client')
    def close_training(self, training_id: str) -> Training:
        """Closes a training.

        Tasks from closed trainings are not assigned to Tolokers.

        Args:
            training_id: The ID of the training to be closed.

        Returns:
            Training: The training with updated status.

        Example:
            >>> opened_training = next(toloka_client.get_trainings(status='OPEN'))
            >>> toloka_client.close_training(training_id=opened_training.id)
            ...
        """
        operation = self.close_training_async(training_id)
        if operation:
            operation = self.wait_operation(operation)
            operation.raise_on_fail()
        return self.get_training(training_id)

    @add_headers('client')
    def close_training_async(self, training_id: str) -> Optional[operations.TrainingCloseOperation]:
        """Closes a training. Sends an asynchronous request to Toloka.

        Tasks from closed trainings are not assigned to Tolokers.

        Args:
            training_id: The ID of the training to be closed.

        Returns:
            TrainingCloseOperation: An object to track the progress of the operation. If the training is already closed then `None` is returned.

        Example:
            >>> opened_training = next(toloka_client.get_trainings(status='OPEN'))
            >>> close_op = toloka_client.close_training_async(training_id=opened_training.id)
            >>> toloka_client.wait_operation(close_op)
            ...
        """
        response = self._raw_request('post', f'/v1/trainings/{training_id}/close')
        # is training already closed?
        if response.status_code == 204:
            return None
        return structure(response.json(), operations.TrainingCloseOperation)

    @add_headers('client')
    def clone_training(self, training_id: str) -> Training:
        """Clones an existing training.

        An empty training with the same parameters is created.
        The new training is attached to the same project.

        Args:
            training_id: The ID of the training to be cloned.

        Returns:
            Training: The new training.

        Example:
            >>> toloka_client.clone_training(training_id='1')
            ...
        """
        operation = self.clone_training_async(training_id)
        operation = self.wait_operation(operation)
        result = self.get_training(operation.details.training_id)
        logger.info(
            f'A new training with ID "{result.id}" has been cloned. Link to open in web interface: '
            f'{self._platform_url}/requester/project/{result.project_id}/training/{result.id}'
        )
        return result

    @add_headers('client')
    def clone_training_async(self, training_id: str) -> operations.TrainingCloneOperation:
        """Clones an existing training. Sends an asynchronous request to Toloka.

        An empty training with the same parameters is created.
        The new training is attached to the same project.

        Args:
            training_id: The ID of the training to be cloned.

        Returns:
            TrainingCloneOperation: An object to track the progress of the operation.

        Example:
            >>> clone_op = toloka_client.clone_training_async(training_id='1')
            >>> toloka_client.wait_operation(clone_op)
            ...
        """
        response = self._request('post', f'/v1/trainings/{training_id}/clone')
        return structure(response, operations.TrainingCloneOperation)

    @add_headers('client')
    def create_training(self, training: Training) -> Training:
        """Creates a new training in Toloka.

        Args:
            training: A training to be created.

        Returns:
            Training: Created training with initialized read-only fields.

        Example:
            Creating a new training.

            >>> new_training = toloka.client.Training(
            >>>     project_id='1',
            >>>     private_name='Some training in my project',
            >>>     may_contain_adult_content=True,
            >>>     assignment_max_duration_seconds=60*5,
            >>>     mix_tasks_in_creation_order=True,
            >>>     shuffle_tasks_in_task_suite=True,
            >>>     training_tasks_in_task_suite_count=3,
            >>>     task_suites_required_to_pass=1,
            >>>     retry_training_after_days=7,
            >>>     inherited_instructions=True,
            >>>     public_instructions='',
            >>> )
            >>> new_training = toloka_client.create_training(new_training)
            >>> print(new_training.id)
            ...
        """
        response = self._request('post', '/v1/trainings', json=unstructure(training))
        result = structure(response, Training)
        logger.info(
            f'A new training with ID "{result.id}" has been created. Link to open in web interface: '
            f'{self._platform_url}/requester/project/{result.project_id}/training/{result.id}'
        )
        return result

    @expand('request')
    @add_headers('client')
    def find_trainings(self, request: search_requests.TrainingSearchRequest,
                       sort: Union[List[str], search_requests.TrainingSortItems, None] = None,
                       limit: Optional[int] = None) -> search_results.TrainingSearchResult:
        """Finds trainings that match certain criteria.

        The number of returned trainings is limited. To find remaining trainings call `find_trainings` with updated search criteria.

        To iterate over all matching trainings you may use the [get_trainings](toloka.client.TolokaClient.get_trainings.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned trainings limit. The maximum allowed limit is 300.

        Returns:
           TrainingSearchResult: Found trainings and a flag showing whether there are more matching trainings exceeding the limit.

        Examples:
            Finding all trainings in all projects.

            >>> trainings = toloka_client.find_trainings()
            ...

            Finding all opened trainings in all projects.

            >>> trainings = toloka_client.find_trainings(status='OPEN')
            ...

            Finding all opened trainings in a specific project.

            >>> trainings = toloka_client.find_trainings(status='OPEN', project_id='1')
            ...

            If there are trainings exceeding the `limit`, then `trainings.has_more` is set to `True`.
        """
        sort = None if sort is None else structure(sort, search_requests.TrainingSortItems)
        response = self._search_request('get', '/v1/trainings', request, sort, limit)
        return structure(response, search_results.TrainingSearchResult)

    @add_headers('client')
    def get_training(self, training_id: str) -> Training:
        """Gets information about a training from Toloka.

        Args:
            training_id: The ID of the training.

        Returns:
            Training: The training.

        Example:
            >>> t = toloka_client.get_training(training_id='1')
            ...
        """
        response = self._request('get', f'/v1/trainings/{training_id}')
        return structure(response, Training)

    @expand('request')
    @add_headers('client')
    def get_trainings(
        self,
        request: search_requests.TrainingSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[Training, None, None]:
        """Finds all trainings that match certain criteria.

        `get_trainings` returns a generator. You can iterate over all found trainings using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort trainings use the [find_trainings](toloka.client.TolokaClient.find_trainings.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned trainings limit for each request. The maximum allowed batch_size is 300.

        Yields:
            Training: The next matching training.

        Example:
            Getting all trainings in a project.

            >>> trainings = toloka_client.get_trainings(project_id='1')
            ...
        """
        generator = self._find_all(self.find_trainings, request, batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def open_training(self, training_id: str) -> Training:
        """Opens a training.

        Tasks from opened trainings can be assigned to Tolokers.

        Args:
            training_id: The ID of the training.

        Returns:
            Training: The training with updated status.

        Example:
            Opening a training.

            >>> toloka_client.open_training(training_id='1')
            ...
        """
        operation = self.open_training_async(training_id)
        if operation:
            operation = self.wait_operation(operation)
            operation.raise_on_fail()
        return self.get_training(training_id)

    @add_headers('client')
    def open_training_async(self, training_id: str) -> Optional[operations.TrainingOpenOperation]:
        """Opens a training. Sends an asynchronous request to Toloka.

        Tasks from opened trainings can be assigned to Tolokers.

        Args:
            training_id: The ID of the training.

        Returns:
            TrainingOpenOperation: An object to track the progress of the operation.
                If the training is already opened then `None` is returned.

        Example:
            Opening a training.

            >>> open_op = toloka_client.open_training_async(training_id='1')
            >>> toloka_client.wait_operation(open_op)
            ...
        """
        response = self._raw_request('post', f'/v1/trainings/{training_id}/open')
        # is training already opened?
        if response.status_code == 204:
            return None
        return structure(response.json(), operations.TrainingOpenOperation)

    @add_headers('client')
    def update_training(self, training_id: str, training: Training) -> Training:
        """Updates parameters of a training in Toloka.

        Args:
            training_id: The ID of the training to be updated.
            training: A training object with new parameter values.

        Returns:
            Training: The updated training.

        Example:
            The example shows how to set new time limit in a training.

            >>> updated_training = toloka_client.get_training(training_id='1')
            >>> updated_training.assignment_max_duration_seconds = 600
            >>> toloka_client.update_training(training_id=updated_training.id, training=updated_training)
            ...
        """
        response = self._request('put', f'/v1/trainings/{training_id}', json=unstructure(training))
        return structure(response, Training)

    # Skills section

    @expand('skill')
    @add_headers('client')
    def create_skill(self, skill: Skill) -> Skill:
        """Creates a new Skill

        You can send a maximum of 10 requests of this kind per minute and 100 requests per day.

        Args:
            skill: New Skill with set parameters.

        Returns:
            Skill: Created skill. With read-only fields.

        Example:
            How to create a new skill.

            >>> new_skill = toloka_client.create_skill(
            >>>     name='Area selection of road signs',
            >>>     public_requester_description={
            >>>         'EN': 'Tolokers annotate road signs',
            >>>         'FR': "Les Tolokers annotent les signaux routier",
            >>>     },
            >>> )
            >>> print(new_skill.id)
            ...
        """
        response = self._request('post', '/v1/skills', json=unstructure(skill))
        result = structure(response, Skill)
        logger.info(
            f'A new skill with ID "{result.id}" has been created. Link to open in web interface: '
            f'{self._platform_url}/requester/quality/skill/{result.id}'
        )
        return result

    @expand('request')
    @add_headers('client')
    def find_skills(self, request: search_requests.SkillSearchRequest,
                    sort: Union[List[str], search_requests.SkillSortItems, None] = None,
                    limit: Optional[int] = None) -> search_results.SkillSearchResult:
        """Finds skills that match certain criteria.

        The number of returned skills is limited. To find remaining skills call `find_skills` with updated search criteria.

        To iterate over all matching skills you may use the [get_skills](toloka.client.TolokaClient.get_skills.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned skills limit. The maximum allowed limit is 100.

        Returns:
           SkillSearchResult: Found skills and a flag showing whether there are more matching skills exceeding the limit.

        Example:
            The example shows how to find ten most recently created skills.

            >>> toloka_client.find_skills(sort=['-created', '-id'], limit=10)
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.SkillSortItems)
        response = self._search_request('get', '/v1/skills', request, sort, limit)
        return structure(response, search_results.SkillSearchResult)

    @add_headers('client')
    def get_skill(self, skill_id: str) -> Skill:
        """Reads one specific skill

        Args:
            skill_id: ID of the skill.

        Returns:
            Skill: The skill.

        Example:
            >>> toloka_client.get_skill(skill_id='1')
            ...
        """
        response = self._request('get', f'/v1/skills/{skill_id}')
        return structure(response, Skill)

    @expand('request')
    @add_headers('client')
    def get_skills(
        self,
        request: search_requests.SkillSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[Skill, None, None]:
        """Finds all skills that match certain criteria.

        `get_skills` returns a generator. You can iterate over all found skills using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort skills use the [find_skills](toloka.client.TolokaClient.find_skills.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned skills limit for each request. The maximum allowed batch_size is 100.

        Yields:
            Skill: The next matching skill.

        Example:
            How to check that a skill exists.

            >>> segmentation_skill = next(toloka_client.get_skills(name='Area selection of road signs'), None)
            >>> if segmentation_skill:
            >>>     print(f'Segmentation skill already exists, with id {segmentation_skill.id}')
            >>> else:
            >>>     print('Create new segmentation skill here')
            ...
        """
        generator = self._find_all(self.find_skills, request, batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def update_skill(self, skill_id: str, skill: Skill) -> Skill:
        """Makes changes to the skill

        Args:
            skill_id: ID of the training that will be changed.
            skill: A skill object with all the fields: those that will be updated and those that will not.

        Returns:
            Skill: Modified skill object with all fields.

        Example:
            >>> toloka_client.update_skill(skill_id=old_skill_id, skill=new_skill_object)
            ...
        """
        response = self._request('put', f'/v1/skills/{skill_id}', json=unstructure(skill))
        return structure(response, Skill)

    # Statistics section

    @add_headers('client')
    def get_analytics(self, stats: List[AnalyticsRequest]) -> operations.AnalyticsOperation:
        """Sends analytics requests to Toloka.

        You can request up to 10 metrics at a time.

        The values of different analytical metrics are returned in the `details` field of the operation when it is completed.

        Args:
            stats: A list of analytics requests.

        Returns:
            operations.AnalyticsOperation: An object to track the progress of the operation.

        Example:
            The example shows how get the percentage of completed tasks in the pool.

            >>> from toloka.client.analytics_request import CompletionPercentagePoolAnalytics
            >>> operation = toloka_client.get_analytics([CompletionPercentagePoolAnalytics(subject_id='1080020')])
            >>> operation = toloka_client.wait_operation(operation)
            >>> print(operation.details['value'][0])
            >>> completed_task_percentage = operation.details['value'][0]['result']['value']
            ...
        """
        response = self._request('post', '/staging/analytics-2', json=unstructure(stats))
        return structure(response, operations.AnalyticsOperation)

    # Task section

    @expand('parameters')
    @add_headers('client')
    def create_task(self, task: Task, parameters: Optional[task.CreateTaskParameters] = None) -> Task:
        """Creates a new task in Toloka.

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

        To create several tasks at once use the [create_tasks](toloka.client.TolokaClient.create_tasks.md) method.

        Args:
            task: The task to be created.
            parameters: Additional parameters of the request.
                Default: `None` — default overlap is used and the pool is started after task creation.

        Returns:
            Task: The created task.

        Example:
            >>> task = toloka.client.Task(
            >>>     input_values={'image': 'https://tlk.s3.yandex.net/dataset/cats_vs_dogs/dogs/048e5760fc5a46faa434922b2447a527.jpg'},
            >>>     pool_id='1'
            >>> )
            >>> toloka_client.create_task(task=task, allow_defaults=True)
            ...
        """
        return self._sync_via_async(
            objects=task,
            parameters=parameters,
            url='/v1/tasks',
            result_type=Task,
            operation_type=operations.TasksCreateOperation,
            output_id_field='task_id',
            get_method=self.get_task,
        )

    @expand('parameters')
    @add_headers('client')
    def create_tasks(
        self,
        tasks: List[Task], parameters: Optional[task.CreateTasksParameters] = None
    ) -> batch_create_results.TaskBatchCreateResult:
        """Creates several tasks in Toloka.

        You can add together general and control tasks.
        Tasks can be added to different pools.
        Note that pools must be configured before accepting new tasks. For example, [mixer configuration](toloka.client.pool.mixer_config.MixerConfig.md) must be set.

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

        By default, `create_tasks` starts asynchronous operation internally and waits for the completion of it. Do not
        change `async_mode` to `False`, if you do not understand clearly why you need it.

        Args:
            tasks: A list of tasks to be created.
            parameters: Additional parameters of the request.

        Returns:
            batch_create_results.TaskBatchCreateResult: The result of the operation.

        Raises:
            ValidationApiError:
                * No tasks were created.
                * Validation errors found while the `skip_invalid_items` parameter was `False`.

        Example:
            The first example shows how to create tasks using a TSV file.

            >>> dataset = pandas.read_csv('dataset.tsv', sep=';')
            >>> tasks = [
            >>>     toloka.client.Task(input_values={'image': url}, pool_id=existing_pool_id)
            >>>     for url in dataset['image'].values[:50]
            >>> ]
            >>> result = toloka_client.create_tasks(tasks, allow_defaults=True)
            >>> print(len(result.items))
            ...

            The second example shows how to add control tasks.

            >>> dataset = pandas.read_csv('labeled_dataset.tsv', sep=';')
            >>> golden_tasks = []
            >>> for _, row in dataset.iterrows():
            >>>     golden_tasks.append(
            >>>         toloka.client.Task(
            >>>             input_values={'image': row['image']},
            >>>             known_solutions = [toloka.client.BaseTask.KnownSolution(output_values={'animal': row['label']})],
            >>>             pool_id = existing_pool_id,
            >>>         )
            >>>     )
            >>> result = toloka_client.create_tasks(golden_tasks, allow_defaults=True)
            >>> print(len(result.items))
            ...
        """
        return self._sync_via_async_pool_related(
            objects=tasks,
            parameters=parameters,
            url='/v1/tasks',
            result_type=batch_create_results.TaskBatchCreateResult,
            operation_type=operations.TasksCreateOperation,
            output_id_field='task_id',
            get_method=self.get_tasks,
        )

    @expand('parameters')
    @add_headers('client')
    def create_tasks_async(self, tasks: List[Task],
                           parameters: Optional[task.CreateTasksParameters] = None) -> operations.TasksCreateOperation:
        """Creates tasks in Toloka asynchronously.

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

        See also the [create_tasks](toloka.client.TolokaClient.create_tasks.md) method.

        Args:
            tasks: A list of tasks to be created.
            parameters: Additional parameters of the request.

        Returns:
            TasksCreateOperation: An object to track the progress of the operation.

        Example:
            >>> training_tasks = [
            >>>     toloka.client.Task(input_values={'image': 'https://some.url/img0.png'}, pool_id='1'),
            >>>     toloka.client.Task(input_values={'image': 'https://some.url/img1.png'}, pool_id='1')
            >>> ]
            >>> tasks_op = toloka_client.create_tasks_async(training_tasks)
            >>> toloka_client.wait_operation(tasks_op)
            ...
        """
        if not parameters.async_mode:
            logger.warning('async_mode=False ignored in TolokaClient.create_tasks_async')
        parameters.async_mode = True
        return self._async_create_objects_idempotent('/v1/tasks', tasks, parameters, operations.TasksCreateOperation)

    @expand('request')
    @add_headers('client')
    def find_tasks(self, request: search_requests.TaskSearchRequest,
                   sort: Union[List[str], search_requests.TaskSortItems, None] = None,
                   limit: Optional[int] = None) -> search_results.TaskSearchResult:
        """Finds tasks that match certain criteria.

        The number of returned tasks is limited. To find remaining tasks call `find_tasks` with updated search criteria.

        To iterate over all matching tasks you may use the [get_tasks](toloka.client.TolokaClient.get_tasks.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned tasks limit. The default limit is 50. The maximum allowed limit is 100,000.

        Returns:
            TaskSearchResult: Found tasks and a flag showing whether there are more matching tasks exceeding the limit.

        Example:
            To find three most recently created tasks in a pool, call the method with the following parameters:

            >>> toloka_client.find_tasks(pool_id='1', sort=['-created', '-id'], limit=3)
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.TaskSortItems)
        response = self._search_request('get', '/v1/tasks', request, sort, limit)
        return structure(response, search_results.TaskSearchResult)

    @add_headers('client')
    def get_task(self, task_id: str) -> Task:
        """Gets a task with specified ID from Toloka.

        Args:
            task_id: The ID of the task.

        Returns:
            Task: The task with the ID specified in the request.

        Example:
            >>> toloka_client.get_task(task_id='1')
            ...
        """
        response = self._request('get', f'/v1/tasks/{task_id}')
        return structure(response, Task)

    @expand('request')
    @add_headers('client')
    def get_tasks(
        self,
        request: search_requests.TaskSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[Task, None, None]:
        """Finds all tasks that match certain criteria.

        `get_tasks` returns a generator. You can iterate over all found tasks using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort tasks use the [find_tasks](toloka.client.TolokaClient.find_tasks.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned tasks limit for each request. The default batch_size is 50. The maximum allowed batch_size is 100,000.

        Yields:
            Task: The next matching task.

        Example:
            Getting all tasks from a single pool.

            >>> results_list = list(toloka_client.get_tasks(pool_id='1'))
            ...
        """
        generator = self._find_all(self.find_tasks, request, batch_size=batch_size)
        yield from generator

    @expand('patch')
    @add_headers('client')
    def patch_task(self, task_id: str, patch: task.TaskPatch) -> Task:
        """Changes a task overlap value.

        Args:
            task_id: The ID of the task.
            patch: New task parameters.

        Returns:
            Task: The task with updated fields.
        """
        response = self._request('patch', f'/v1/tasks/{task_id}', json=unstructure(patch))
        return structure(response, Task)

    @expand('patch')
    @add_headers('client')
    def patch_task_overlap_or_min(self, task_id: str, patch: task.TaskOverlapPatch) -> Task:
        """Stops assigning a task to Tolokers.

        Args:
            task_id: The ID of the task.
            patch: New overlap value.

        Returns:
            Task: The task with updated fields.

        Example:
            Setting an infinite overlap for a training task.

            >>> toloka_client.patch_task_overlap_or_min(task_id='1', infinite_overlap=True)
            ...

            {% note info %}

            You can't set infinite overlap in a regular pool.

            {% endnote %}
        """
        response = self._request('patch', f'/v1/tasks/{task_id}/set-overlap-or-min', json=unstructure(patch))
        return structure(response, Task)

    # Task suites section

    @expand('parameters')
    @add_headers('client')
    def create_task_suite(
        self,
        task_suite: TaskSuite, parameters: Optional[task_suite.TaskSuiteCreateRequestParameters] = None
    ) -> TaskSuite:
        """Creates a task suite in Toloka.

        Usually, you don't need to create a task suite manually, because Toloka can group tasks into suites automatically.

        Use this method if you need to group specific tasks together or to set different parameters in different task suites.

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        To create several task suites at once use the [create_task_suites](toloka.client.TolokaClient.create_task_suites.md) method.

        Args:
            task_suite: A task suite to be created.
            parameters: Additional parameters of the request. Default: `None`

        Returns:
            TaskSuite: Created task suite.

        Example:
            >>> new_task_suite = toloka.client.TaskSuite(
            >>>     pool_id='1',
            >>>     tasks=[toloka.client.Task(input_values={'label': 'Cats vs Dogs'})],
            >>>     overlap=2
            >>> )
            >>> toloka_client.create_task_suite(new_task_suite)
            ...
        """
        return self._sync_via_async(
            objects=task_suite,
            parameters=parameters,
            url='/v1/task-suites',
            result_type=TaskSuite,
            operation_type=operations.TaskSuiteCreateBatchOperation,
            output_id_field='task_suite_id',
            get_method=self.get_task_suite,
        )

    @expand('parameters')
    @add_headers('client')
    def create_task_suites(
        self,
        task_suites: List[TaskSuite], parameters: Optional[task_suite.TaskSuitesCreateRequestParameters] = None
    ) -> batch_create_results.TaskSuiteBatchCreateResult:
        """Creates several task suites in Toloka.

        Usually, you don't need to create a task suite manually, because Toloka can group tasks into suites automatically.

        Use this method if you need to group specific tasks together or to set different parameters in different task suites.
        Task suites can be created in different pools. You can create general and control tasks or task suites in different pools with a single method call.

        By default, `create_task_suites` starts asynchronous operation internally and waits for the completion of it. Do not
        change `async_mode` to `False`, if you do not understand clearly why you need it.

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        It is recommended that you create no more than 10,000 task suites in a single request if the `async_mode` parameter is `True`.

        Args:
            task_suites: A list of task suites to be created.
            parameters: Additional parameters of the request. Default: `None`

        Returns:
            TaskSuiteBatchCreateResult: The result of the operation.

        Raises:
            ValidationApiError:
                * No tasks were created.
                * Validation errors found while the `skip_invalid_items` parameter was `False`.

        Example:
            >>> task_suites = [
            >>>     toloka.client.TaskSuite(
            >>>         pool_id=1,
            >>>         overlap=1,
            >>>         tasks=[
            >>>             toloka.client.Task(input_values={
            >>>                 'question': 'Choose a random number'
            >>>             })
            >>>         ]
            >>>     )
            >>> ]
            >>> task_suites = toloka_client.create_task_suites(task_suites)
            ...
        """
        return self._sync_via_async_pool_related(
            objects=task_suites,
            parameters=parameters,
            url='/v1/task-suites',
            result_type=batch_create_results.TaskSuiteBatchCreateResult,
            operation_type=operations.TaskSuiteCreateBatchOperation,
            output_id_field='task_suite_id',
            get_method=self.get_task_suites,
        )

    @expand('parameters')
    @add_headers('client')
    def create_task_suites_async(
        self,
        task_suites: List[TaskSuite], parameters: Optional[task_suite.TaskSuitesCreateRequestParameters] = None
    ) -> operations.TaskSuiteCreateBatchOperation:
        """Creates several task suites in Toloka asynchronously.

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        It is recommended that you create no more than 10,000 task suites in a single request.

        See also the [create_task_suites](toloka.client.TolokaClient.create_task_suites.md) method.

        Args:
            task_suites: A list of task suites to be created.
            parameters: Additional parameters of the request. Default: `None`

        Returns:
            TaskSuiteCreateBatchOperation: An object to track the progress of the operation.

        Example:
            >>> task_suites = [
            >>>     toloka.client.TaskSuite(
            >>>         pool_id='1',
            >>>         overlap=1,
            >>>         tasks=[
            >>>             toloka.client.Task(input_values={
            >>>                 'question': 'Choose a random country'
            >>>             })
            >>>         ]
            >>>     )
            >>> ]
            >>> task_suites_op = toloka_client.create_task_suites_async(task_suites)
            >>> toloka_client.wait_operation(task_suites_op)
            ...
        """
        if not parameters.async_mode:
            logger.warning('async_mode=False ignored in TolokaClient.create_task_suites_async')
        parameters.async_mode = True
        return self._async_create_objects_idempotent(
            '/v1/task-suites', task_suites, parameters, operations.TaskSuiteCreateBatchOperation
        )

    @expand('request')
    @add_headers('client')
    def find_task_suites(
        self, request: search_requests.TaskSuiteSearchRequest,
        sort: Union[List[str], search_requests.TaskSuiteSortItems, None] = None, limit: Optional[int] = None
    ) -> search_results.TaskSuiteSearchResult:
        """Finds task suites that match certain criteria.

        The number of returned task suites is limited. To find remaining task suites call `find_task_suites` with updated search criteria.

        To iterate over all matching task suites you may use the [get_task_suites](toloka.client.TolokaClient.get_task_suites.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned task suites limit. The default limit is 50. The maximum allowed limit is 100,000.

        Returns:
            TaskSuiteSearchResult: Found task suites and a flag showing whether there are more matching task suites exceeding the limit.

        Example:
            Find three most recently created task suites in a specified pool.

            >>> toloka_client.find_task_suites(pool_id='1', sort=['-created', '-id'], limit=3)
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.TaskSuiteSortItems)
        response = self._search_request('get', '/v1/task-suites', request, sort, limit)
        return structure(response, search_results.TaskSuiteSearchResult)

    @add_headers('client')
    def get_task_suite(self, task_suite_id: str) -> TaskSuite:
        """Reads one task suite.

        Args:
            task_suite_id: ID of the task suite.

        Returns:
            TaskSuite: The task suite.

        Example:
            >>> toloka_client.get_task_suite(task_suite_id='1')
            ...
        """
        response = self._request('get', f'/v1/task-suites/{task_suite_id}')
        return structure(response, TaskSuite)

    @expand('request')
    @add_headers('client')
    def get_task_suites(
        self,
        request: search_requests.TaskSuiteSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[TaskSuite, None, None]:
        """Finds all task suites that match certain criteria.

        `get_task_suites` returns a generator. You can iterate over all found task suites using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort task suites use the [find_task_suites](toloka.client.TolokaClient.find_task_suites.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned task suites limit for each request. The default batch_size is 50. The maximum allowed batch_size is 100,000.

        Yields:
            TaskSuite: The next matching task suite.

        Example:
            Get task suites from a specific pool.

            >>> results_list = list(toloka_client.get_task_suites(pool_id='1'))
            ...
        """
        generator = self._find_all(self.find_task_suites, request, batch_size=batch_size)
        yield from generator

    @expand('patch')
    @add_headers('client')
    def patch_task_suite(self, task_suite_id: str, patch: task_suite.TaskSuitePatch) -> TaskSuite:
        """Changes task suite parameter values in Toloka.

        Args:
            task_suite_id: The ID of the task suite.
            patch: New parameter values.

        Returns:
            TaskSuite: The task suite with updated fields.

        Example:
            Change the task suite's priority.

            >>> toloka_client.patch_task_suite(task_suite_id='1', issuing_order_override=100)
            ...
        """
        body = unstructure(patch)
        params = {'open_pool': body.pop('open_pool')} if 'open_pool' in body else None
        response = self._request('patch', f'/v1/task-suites/{task_suite_id}', json=body, params=params)
        return structure(response, TaskSuite)

    @expand('patch')
    @add_headers('client')
    def patch_task_suite_overlap_or_min(self, task_suite_id: str, patch: task_suite.TaskSuiteOverlapPatch) -> TaskSuite:
        """Stops issuing the task suites

        Args:
            task_suite_id: ID of the task suite.
            patch: New overlap value.

        Returns:
            TaskSuite: Task suite with updated fields.

        Example:
            >>> toloka_client.patch_task_suite_overlap_or_min(task_suite_id='1', overlap=100)
            ...
        """
        body = unstructure(patch)
        params = {'open_pool': body.pop('open_pool')} if 'open_pool' in body else None
        response = self._request('patch', f'/v1/task-suites/{task_suite_id}/set-overlap-or-min', json=body, params=params)
        return structure(response, TaskSuite)

    # Operations section

    @add_headers('client')
    def get_operation(self, operation_id: str) -> operations.Operation:
        """Reads information about operation

        All asynchronous actions in Toloka works via operations. If you have some "Operation" usually you need to use
        "wait_operation" method.

        Args:
            operation_id: ID of the operation.

        Returns:
            Operation: The operation.

        Example:
            >>> op = toloka_client.get_operation(operation_id='1')
            ...
        """
        response = self._request('get', f'/v1/operations/{operation_id}')
        return structure(response, operations.Operation)

    @add_headers('client')
    def wait_operation(
        self,
        op: operations.Operation, timeout: datetime.timedelta = datetime.timedelta(minutes=10),
        disable_progress: bool = False
    ) -> operations.Operation:
        """Waits for the operation to complete, and return it

        Args:
            op: ID of the operation.
            timeout: How long to wait. Defaults to 10 minutes.
            disable_progress: Whether disable progress bar or enable. Defaults to `False` (meaning progress bar is shown).

        Raises:
            TimeoutError: Raises it if the timeout has expired and the operation is still not completed.

        Returns:
            Operation: Completed operation.

        Example:
            Waiting for the pool to close can be running in the background.

            >>> pool = toloka_client.get_pool(pool_id)
            >>> while not pool.is_closed():
            >>>     op = toloka_client.get_analytics(
            >>>         [toloka.analytics_request.CompletionPercentagePoolAnalytics(subject_id=pool.id)]
            >>>     )
            >>>     op = toloka_client.wait_operation(op)
            >>>     percentage = op.details['value'][0]['result']['value']
            >>>     print(
            >>>         f'{datetime.datetime.now().strftime("%H:%M:%S")}'
            >>>         f'Pool {pool.id} - {percentage}%'
            >>>     )
            >>>     time.sleep(60 * minutes_to_wait)
            >>>     pool = toloka_client.get_pool(pool.id)
            >>> print('Pool was closed.')
            ...
        """
        default_time_to_wait = datetime.timedelta(seconds=1)
        default_initial_delay = datetime.timedelta(milliseconds=500)

        if op.is_completed():
            return op

        utcnow = datetime.datetime.now(datetime.timezone.utc)
        wait_until_time = utcnow + timeout

        with logging_redirect_tqdm():
            with tqdm(total=100, disable=disable_progress) as progress_bar:
                progress = 0

                if not op.started or utcnow - op.started < default_initial_delay:
                    time.sleep(default_initial_delay.total_seconds())

                while True:
                    op = self.get_operation(op.id)
                    progress_bar.update(op.progress - progress if op.progress else 0)
                    progress = op.progress if op.progress else 0
                    if op.is_completed():
                        progress_bar.update(100 - progress)
                        return op
                    time.sleep(default_time_to_wait.total_seconds())
                    if datetime.datetime.now(datetime.timezone.utc) > wait_until_time:
                        raise TimeoutError

    @expand('request')
    @add_headers('client')
    def find_operations(
        self, request: search_requests.OperationSearchRequest,
        sort: Union[List[str], search_requests.OperationSortItems, None] = None, limit: Optional[int] = None
    ) -> search_results.OperationSearchResult:
        """Finds operations that match certain criteria.

        The number of returned operations is limited. To find remaining operations call `find_operations` with updated search criteria.

        To iterate over all matching operations you may use the [get_operations](toloka.client.TolokaClient.get_operations.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned operations limit. The default limit is 50. The maximum allowed limit is 500.

        Returns:
            OperationSearchResult: Found operations and a flag showing whether there are more matching task suites exceeding the limit.

        Example:
            >>> toloka_client.find_operations(type='POOL_OPEN', status='SUCCESS', sort=['-finished'], limit=3)
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.OperationSortItems)
        response = self._search_request('get', '/v1/operations', request, sort, limit)
        return structure(response, search_results.OperationSearchResult)

    @expand('request')
    @add_headers('client')
    def get_operations(
        self,
        request: search_requests.OperationSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[operations.Operation, None, None]:
        """Finds all operations that match certain rules and returns them in an iterable object

        `get_operations` returns a generator. You can iterate over all found operations using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort operations use the [find_operations](toloka.client.TolokaClient.find_operations.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned operations limit for each request. The default batch_size is 50. The maximum allowed batch_size is 500.

        Yields:
            Operation: The next matching operations.

        Example:
            >>> bonuses = list(toloka_client.get_operations(submitted_lt='2021-06-01T00:00:00'))
            ...
        """
        generator = self._find_all(self.find_operations, request, batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def get_operation_log(self, operation_id: str) -> List[OperationLogItem]:
        """Reads information about validation errors and which task (or task suites) were created

        You don't need to call this method if you use "create_tasks" for creating tasks ("create_task_suites" for task suites).
        By asynchronous creating multiple tasks (or task sets) you can get the operation log.
        Logs are only available for the last month.

        Args:
            operation_id: ID of the operation.

        Returns:
            List[OperationLogItem]: Logs for the operation.

        Example:
            >>> op = toloka_client.get_operation_log(operation_id='1')
            ...
        """
        response = self._request('get', f'/v1/operations/{operation_id}/log')
        return structure(response, List[OperationLogItem])

    # User bonus

    @expand('parameters')
    @add_headers('client')
    def create_user_bonus(
        self,
        user_bonus: UserBonus, parameters: Optional[user_bonus.UserBonusCreateRequestParameters] = None
    ) -> UserBonus:
        """Issues payments directly to a Toloker.

        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonus: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonus: Created bonus.

        Example:
            Create bonus for specific assignment.

            >>> import decimal
            >>> new_bonus = toloka_client.create_user_bonus(
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title={
            >>>             'EN': 'Perfect job!',
            >>>             'RU': 'Прекрасная работа!',
            >>>         },
            >>>         public_message={
            >>>             'EN': 'You are the best!',
            >>>             'RU': 'Молодец!',
            >>>         },
            >>>         assignment_id='012345'
            >>>     )
            >>> )
            ...
        """
        return self._sync_via_async(
            objects=user_bonus,
            parameters=parameters,
            url='/v1/user-bonuses',
            result_type=UserBonus,
            operation_type=operations.UserBonusCreateBatchOperation,
            output_id_field='user_bonus_id',
            get_method=self.get_user_bonus,
        )

    @expand('parameters')
    @add_headers('client')
    def create_user_bonuses(
        self,
        user_bonuses: List[UserBonus], parameters: Optional[user_bonus.UserBonusesCreateRequestParameters] = None
    ) -> batch_create_results.UserBonusBatchCreateResult:
        """Creates bonuses for Tolokers.

        Right now it's safer to use asynchronous version: "create_user_bonuses_async"
        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonuses: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonusBatchCreateResult: Result of creating bonuses. Contains `UserBonus` instances in `items` and
                problems in `validation_errors`.

        Example:
            >>> import decimal
            >>> new_bonuses=[
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title={
            >>>             'EN': 'Perfect job!',
            >>>             'RU': 'Прекрасная работа!',
            >>>         },
            >>>         public_message={
            >>>             'EN': 'You are the best!',
            >>>             'RU': 'Молодец!',
            >>>         },
            >>>         assignment_id='1'
            >>>     ),
            >>>     UserBonus(
            >>>         user_id='2',
            >>>         amount=decimal.Decimal('1.0'),
            >>>         public_title={
            >>>             'EN': 'Excellent work!',
            >>>             'RU': 'Отличная работа!',
            >>>         },
            >>>         public_message={
            >>>             'EN': 'You have completed all tasks!',
            >>>             'RU': 'Сделаны все задания!',
            >>>         },
            >>>         assignment_id='2'
            >>>     )
            >>> ]
            >>> toloka_client.create_user_bonuses(new_bonuses)
            ...
        """
        return self._sync_via_async(
            objects=user_bonuses,
            parameters=parameters,
            url='/v1/user-bonuses',
            result_type=batch_create_results.UserBonusBatchCreateResult,
            operation_type=operations.UserBonusCreateBatchOperation,
            output_id_field='user_bonus_id',
            get_method=self.get_user_bonuses,
        )

    @expand('parameters')
    @add_headers('client')
    def create_user_bonuses_async(
        self, user_bonuses: List[UserBonus], parameters: Optional[user_bonus.UserBonusesCreateRequestParameters] = None
    ) -> operations.UserBonusCreateBatchOperation:
        """Issues payments directly to Tolokers, asynchronously creates many `UserBonus` instances.

        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonuses: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonusCreateBatchOperation: An operation upon completion of which the bonuses can be considered created.

        Example:
            >>> import decimal
            >>> new_bonuses=[
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount=decimal.Decimal('0.50'),
            >>>         public_title={
            >>>             'EN': 'Perfect job!',
            >>>             'RU': 'Прекрасная работа!',
            >>>         },
            >>>         public_message={
            >>>             'EN': 'You are the best!',
            >>>             'RU': 'Молодец!',
            >>>         },
            >>>         assignment_id='1'
            >>>     ),
            >>>     UserBonus(
            >>>         user_id='2',
            >>>         amount=decimal.Decimal('1.0'),
            >>>         public_title={
            >>>             'EN': 'Excellent work!',
            >>>             'RU': 'Превосходная работа!',
            >>>         },
            >>>         public_message={
            >>>             'EN': 'You have completed all tasks!',
            >>>             'RU': 'Сделаны все задания!',
            >>>         },
            >>>         assignment_id='2'
            >>>     )
            >>> ]
            >>> create_bonuses = toloka_client.create_user_bonuses_async(new_bonuses)
            >>> toloka_client.wait_operation(create_bonuses)
            ...
        """
        if not parameters.async_mode:
            logger.warning('async_mode=False ignored in TolokaClient.create_user_bonuses_async')
        parameters.async_mode = True
        return self._async_create_objects_idempotent(
            '/v1/user-bonuses', user_bonuses, parameters, operations.UserBonusCreateBatchOperation
        )

    @expand('request')
    @add_headers('client')
    def find_user_bonuses(self, request: search_requests.UserBonusSearchRequest,
                          sort: Union[List[str], search_requests.UserBonusSortItems, None] = None,
                          limit: Optional[int] = None) -> search_results.UserBonusSearchResult:
        """Finds Tolokers' bonuses that match certain criteria.

        The number of returned bonuses is limited. To find remaining bonuses call `find_user_bonuses` with updated search criteria.

        To iterate over all matching Tolokers' bonuses you may use the [get_user_bonuses](toloka.client.TolokaClient.get_user_bonuses.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned Tolokers' bonuses limit. The maximum allowed limit is 300.

        Returns:
            UserBonusSearchResult: Found Tolokers' bonuses and a flag showing whether there are more matching bonuses exceeding the limit.

        Example:
            >>> toloka_client.find_user_bonuses(user_id='1', sort=['-created', '-id'], limit=3)
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.UserBonusSortItems)
        response = self._search_request('get', '/v1/user-bonuses', request, sort, limit)
        return structure(response, search_results.UserBonusSearchResult)

    @add_headers('client')
    def get_user_bonus(self, user_bonus_id: str) -> UserBonus:
        """Gets information about a Toloker's bonus.

        Args:
            user_bonus_id: The ID of the bonus.

        Returns:
            UserBonus: The information about the bonus.

        Example:
            >>> toloka_client.get_user_bonus(user_bonus_id='1')
            ...
        """
        response = self._request('get', f'/v1/user-bonuses/{user_bonus_id}')
        return structure(response, UserBonus)

    @expand('request')
    @add_headers('client')
    def get_user_bonuses(
        self,
        request: search_requests.UserBonusSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[UserBonus, None, None]:
        """Finds all Tolokers' bonuses that match certain rules and returns them in an iterable object

        `get_user_bonuses` returns a generator. You can iterate over all found Tolokers' bonuses using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort bonuses use the [find_user_bonuses](toloka.client.TolokaClient.find_user_bonuses.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned Tolokers' bonuses limit for each request. The maximum allowed `batch_size` is 300.

        Yields:
            UserBonus: The next matching Toloker's bonus.

        Example:
            >>> bonuses = list(toloka_client.get_user_bonuses(created_lt='2021-06-01T00:00:00'))
            ...
        """
        generator = self._find_all(self.find_user_bonuses, request, batch_size=batch_size)
        yield from generator

    # User restrictions

    @expand('request')
    @add_headers('client')
    def find_user_restrictions(self, request: search_requests.UserRestrictionSearchRequest,
                               sort: Union[List[str], search_requests.UserRestrictionSortItems, None] = None,
                               limit: Optional[int] = None) -> search_results.UserRestrictionSearchResult:
        """Finds Toloker restrictions that match certain criteria.

        The number of returned restrictions is limited. To find remaining restrictions call `find_user_restrictions` with updated search criteria.

        To iterate over all matching Toloker restrictions you may use the [get_user_restrictions](toloka.client.TolokaClient.get_user_restrictions.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned Toloker restrictions limit. The maximum allowed limit is 500.

        Returns:
            UserRestrictionSearchResult: Found Toloker restrictions and a flag showing whether there are more matching restrictions exceeding the limit.

        Example:
            >>> restrictions = toloka_client.find_user_restrictions(sort=['-created', '-id'], limit=10)
            ...

            If there are restrictions exceeding the `limit`, then `restrictions.has_more` is set to `True`.
        """
        sort = None if sort is None else structure(sort, search_requests.UserRestrictionSortItems)
        response = self._search_request('get', '/v1/user-restrictions', request, sort, limit)
        return structure(response, search_results.UserRestrictionSearchResult)

    @add_headers('client')
    def get_user_restriction(self, user_restriction_id: str) -> UserRestriction:
        """Gets information about a Toloker restriction.

        Args:
            user_restriction_id: ID of the Toloker restriction.

        Returns:
            UserRestriction: The Toloker restriction.

        Example:
            >>> toloka_client.get_user_restriction(user_restriction_id='1')
            ...
        """
        response = self._request('get', f'/v1/user-restrictions/{user_restriction_id}')
        return structure(response, UserRestriction)

    @expand('request')
    @add_headers('client')
    def get_user_restrictions(
        self,
        request: search_requests.UserRestrictionSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[UserRestriction, None, None]:
        """Finds all Toloker restrictions that match certain criteria.

        `get_user_restrictions` returns a generator. You can iterate over all found Toloker restrictions using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort Toloker restrictions use the [find_user_restrictions](toloka.client.TolokaClient.find_user_restrictions.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned Toloker restrictions limit for each request. The maximum allowed batch_size is 500.

        Yields:
            UserRestriction: The next matching Toloker restriction.

        Example:
            >>> results_list = list(toloka_client.get_user_restrictions(scope='ALL_PROJECTS'))
            ...
        """
        generator = self._find_all(self.find_user_restrictions, request, batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def set_user_restriction(self, user_restriction: UserRestriction) -> UserRestriction:
        """Restricts access to projects or pools for a Toloker.

        Args:
            user_restriction: Restriction parameters.

        Returns:
            UserRestriction: Updated restriction object.

        Example:
            If a Toloker often makes mistakes, we will restrict access to all our projects.

            >>> new_restriction = toloka_client.set_user_restriction(
            >>>     toloka.user_restriction.ProjectUserRestriction(
            >>>         user_id='1',
            >>>         private_comment='The Toloker often makes mistakes',
            >>>         project_id='5'
            >>>     )
            >>> )
            ...
        """
        response = self._request('put', '/v1/user-restrictions', json=unstructure(user_restriction))
        return structure(response, UserRestriction)

    @add_headers('client')
    def delete_user_restriction(self, user_restriction_id: str) -> None:
        """Unlocks existing restriction

        Args:
            user_restriction_id: Restriction that should be removed.

        Example:
            >>> toloka_client.delete_user_restriction(user_restriction_id='1')
            ...
        """
        self._raw_request('delete', f'/v1/user-restrictions/{user_restriction_id}')

    # Requester

    @add_headers('client')
    def get_requester(self) -> Requester:
        """Reads information about the customer and the account balance

        Returns:
            Requester: Object that contains all information about customer.

        Examples:
            Make sure that you've entered a valid OAuth token.

            >>> toloka_client.get_requester()
            ...

            You can also estimate approximate pipeline costs and check if there is enough money on your account.

            >>> requester = toloka_client.get_requester()
            >>> if requester.balance >= approx_pipeline_price:
            >>>     print('You have enough money on your account!')
            >>> else:
            >>>     print("You haven't got enough money on your account!")
            ...
        """
        response = self._request('get', '/v1/requester')
        return structure(response, Requester)

    # User skills

    @expand('request')
    @add_headers('client')
    def find_user_skills(self, request: search_requests.UserSkillSearchRequest,
                         sort: Union[List[str], search_requests.UserSkillSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.UserSkillSearchResult:
        """Finds Toloker's skills that match certain criteria.

        The number of returned Toloker's skills is limited. To find remaining skills call `find_user_skills` with updated search criteria.

        To iterate over all matching skills you may use the [get_user_skills](toloka.client.TolokaClient.get_user_skills.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned skills limit. The maximum allowed limit is 1000.

        Returns:
            UserSkillSearchResult: Found Toloker's skills and a flag showing whether there are more matching skills exceeding the limit.

        Example:
            >>> skills = toloka_client.find_user_skills(limit=10)
            ...

            If there are skills exceeding the `limit`, then `skills.has_more` is set to `True`.
        """
        sort = None if sort is None else structure(sort, search_requests.UserSkillSortItems)
        response = self._search_request('get', '/v1/user-skills', request, sort, limit)
        return structure(response, search_results.UserSkillSearchResult)

    @add_headers('client')
    def get_user_skill(self, user_skill_id: str) -> UserSkill:
        """Gets the value of a Toloker's skill

        `UserSkill` describes the skill value for a specific Toloker.

        Args:
            user_skill_id: The ID of the Toloker skill.

        Returns:
            UserSkill: The skill value.

        Example:
            >>> toloka_client.get_user_skill(user_skill_id='1')
            ...
        """
        response = self._request('get', f'/v1/user-skills/{user_skill_id}')
        return structure(response, UserSkill)

    @expand('request')
    @add_headers('client')
    def get_user_skills(
        self,
        request: search_requests.UserSkillSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[UserSkill, None, None]:
        """Finds all Toloker's skills that match certain criteria.

        `get_user_skills` returns a generator. You can iterate over all found Toloker's skills using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort Toloker's skills use the [find_user_skills](toloka.client.TolokaClient.find_user_skills.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned skills limit for each request. The maximum allowed batch_size is 1000.

        Yields:
            UserSkill: The next matching Toloker's skill.

        Example:
            >>> results_list = list(toloka_client.get_user_skills())
            ...
        """
        generator = self._find_all(self.find_user_skills, request, batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def get_user(self, user_id: str) -> User:
        """Gets Toloker metadata by `user_id`.

        Args:
            user_id: Toloker ID.

        Returns:
            User: Contains Toloker metadata.
        """

        response = self._request('get', f'/v1/user-metadata/{user_id}')
        return structure(response, User)

    @expand('request')
    @add_headers('client')
    def set_user_skill(self, request: SetUserSkillRequest) -> UserSkill:
        """Assigns a skill to a Toloker.

        Args:
            request: Skill parameters.

        Returns:
            UserSkill: Updated skill information.

        Example:
            >>> from decimal import Decimal
            >>> toloka_client.set_user_skill(skill_id='1', user_id='1', value=Decimal(100))
            ...
        """
        response = self._request('put', '/v1/user-skills', json=unstructure(request))
        return structure(response, UserSkill)

    @add_headers('client')
    def delete_user_skill(self, user_skill_id: str) -> None:
        """Drop specific UserSkill

        `UserSkill` describes the skill value for a specific Toloker.

        Args:
            user_skill_id: ID of the fact that the Toloker has a skill to delete.

        Example:
            >>> toloka_client.delete_user_skill(user_skill_id='1')
            ...
        """
        self._raw_request('delete', f'/v1/user-skills/{user_skill_id}')

    @add_headers('client')
    def upsert_webhook_subscriptions(
        self,
        subscriptions: List[WebhookSubscription]
    ) -> batch_create_results.WebhookSubscriptionBatchCreateResult:
        """Creates (upsert) webhook subscriptions.

        Args:
            subscriptions: A list of webhook subscriptions to be created.

        Returns:
            batch_create_results.WebhookSubscriptionBatchCreateResult: The result of the operation.

        Raises:
            ValidationApiError: No subscriptions were created.

        Example:
            How to create several subscriptions.

            >>> created_result = toloka_client.upsert_webhook_subscriptions([
            >>>     {
            >>>         'webhook_url': 'https://awesome-requester.com/toloka-webhook',
            >>>         'event_type': toloka.webhook_subscription.WebhookSubscription.EventType.ASSIGNMENT_CREATED,
            >>>         'pool_id': '121212'
            >>>     },
            >>>     {
            >>>         'webhook_url': 'https://awesome-requester.com/toloka-webhook',
            >>>         'event_type': toloka.webhook_subscription.WebhookSubscription.EventType.POOL_CLOSED,
            >>>         'pool_id': '121212',
            >>>     }
            >>> ])
            >>> print(len(created_result.items))
            ...
        """
        response = self._request('put', '/v1/webhook-subscriptions', json=unstructure(subscriptions))
        return structure(response, batch_create_results.WebhookSubscriptionBatchCreateResult)

    @add_headers('client')
    def get_webhook_subscription(self, webhook_subscription_id: str) -> WebhookSubscription:
        """Get one specific webhook-subscription

        Args:
            webhook_subscription_id: ID of the subscription.

        Returns:
            WebhookSubscription: The subscription.
        """
        response = self._request('get', f'/v1/webhook-subscriptions/{webhook_subscription_id}')
        return structure(response, WebhookSubscription)

    @expand('request')
    @add_headers('client')
    def find_webhook_subscriptions(self, request: search_requests.WebhookSubscriptionSearchRequest,
                                   sort: Union[List[str], search_requests.WebhookSubscriptionSortItems, None] = None,
                                   limit: Optional[int] = None) -> search_results.WebhookSubscriptionSearchResult:
        """Finds webhook subscriptions that match certain criteria.

        The number of returned webhook subscriptions is limited. To find remaining webhook subscriptions call `find_webhook_subscriptions` with updated search criteria.

        To iterate over all matching webhook subscriptions you may use the [get_webhook_subscriptions](toloka.client.TolokaClient.get_webhook_subscriptions.md) method.

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned webhook subscriptions limit. The maximum allowed limit is 300.

        Returns:
            WebhookSubscriptionSearchResult: Found webhook subscriptions and a flag showing whether there are more matching webhook subscriptions exceeding the limit.
        """
        sort = None if sort is None else structure(sort, search_requests.WebhookSubscriptionSortItems)
        response = self._search_request('get', '/v1/webhook-subscriptions', request, sort, limit)
        return structure(response, search_results.WebhookSubscriptionSearchResult)

    @expand('request')
    @add_headers('client')
    def get_webhook_subscriptions(
        self,
        request: search_requests.WebhookSubscriptionSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[WebhookSubscription, None, None]:
        """Finds all webhook subscriptions that match certain criteria.

        `get_webhook_subscriptions` returns a generator. You can iterate over all found webhook subscriptions using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort webhook subscriptions use the [find_webhook_subscriptions](toloka.client.TolokaClient.find_webhook_subscriptions.md) method.

        Args:
            request: Search criteria.
            batch_size: Returned webhook subscriptions limit for each request. The maximum allowed batch_size is 300.

        Yields:
            WebhookSubscription: The next matching webhook subscription.
        """
        generator = self._find_all(self.find_webhook_subscriptions, request, sort_field='created', batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def delete_webhook_subscription(self, webhook_subscription_id: str) -> None:
        """Drop specific webhook-subscription

        Args:
            webhook_subscription_id: ID of the webhook-subscription to delete.
        """
        self._raw_request('delete', f'/v1/webhook-subscriptions/{webhook_subscription_id}')

    # Experimental section

    if PANDAS_INSTALLED:
        @expand('parameters')
        @add_headers('client')
        def get_assignments_df(self, pool_id: str, parameters: GetAssignmentsTsvParameters) -> pd.DataFrame:
            """Downloads assignments as pandas.DataFrame.

            {% note warning %}

            Requires toloka-kit[pandas] extras. Install it with the following command:

            ```shell
            pip install toloka-kit[pandas]
            ```

            {% endnote %}

            Experimental method.
            Implements the same behavior as if you download results in web-interface and then read it by pandas.

            Args:
                pool_id: From which pool the results are loaded.
                parameters: Filters for the results and the set of fields that will be in the dataframe.

            Returns:
                pd.DataFrame: DataFrame with all results. Contains groups of fields with prefixes:
                    * "INPUT" - Fields that were at the input in the task.
                    * "OUTPUT" - Fields that were received as a result of execution.
                    * "GOLDEN" - Fields with correct answers. Filled in only for golden tasks and training tasks.
                    * "HINT" - Hints for completing tasks. Filled in for training tasks.
                    * "ACCEPT" - Fields describing the deferred acceptance of tasks.
                    * "ASSIGNMENT" - fields describing additional information about the Assignment.

            Example:
                Get all assignments from the specified pool by `pool_id` to [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).
                And apply the native pandas `rename` method to change columns' names.

                >>> answers_df = toloka_client.get_assignments_df(pool_id='1')
                >>> answers_df = answers_df.rename(columns={
                >>>     'INPUT:image': 'task',
                >>>     'OUTPUT:result': 'label',
                >>>     'ASSIGNMENT:worker_id': 'annotator'
                >>> })
                ...
            """
            logger.warning('Experimental method')
            response = self._raw_request('get', f'/new/requester/pools/{pool_id}/assignments.tsv',
                                         params=unstructure(parameters))
            return pd.read_csv(io.StringIO(response.text), delimiter='\t')
    else:
        def get_assignments_df(self, *args, **kwargs):
            raise NotImplementedError('Please install toloka-kit[pandas] extras.')

    # toloka apps

    @expand('request')
    @add_headers('client')
    def find_app_projects(self, request: search_requests.AppProjectSearchRequest,
                          sort: Union[List[str], search_requests.AppProjectSortItems, None] = None,
                          limit: Optional[int] = None) -> search_results.AppProjectSearchResult:
        """Finds App projects that match certain criteria.

        The number of returned projects is limited. To find remaining projects call `find_app_projects` with updated search criteria.

        To iterate over all matching projects you may use the [get_app_projects](toloka.client.TolokaClient.get_app_projects.md) method.

        Example:
            Searching active projects based on the App solution with the specified ID.

            >>> search = toloka_client.find_app_projects(
            >>>     app_id = '9lZaMl363jahzra1rrYq', status = 'READY')
            >>> for app_project in search.content:
            >>>     print(app_project.id, app_project.name)
            >>>
            >>> if search.has_more:
            >>>     print('There are more App projects...')
            ...

        Args:
            request: Search criteria.
            sort: The order and direction of sorting the results.
            limit: Returned projects limit. The maximum limit is 5000.

        Returns:
            AppProjectSearchResult: Found projects and a flag showing whether there are more matching projects exceeding the limit.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        sort = None if sort is None else structure(sort, search_requests.AppProjectSortItems)
        response = self._search_request('get', '/app/v0/app-projects', request, sort, limit)
        return structure(response, search_results.AppProjectSearchResult)

    @expand('request')
    @add_headers('client')
    def get_app_projects(
        self,
        request: search_requests.AppProjectSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[AppProject, None, None]:
        """Finds all App projects that match certain criteria.

        `get_app_projects` returns a generator. You can iterate over all found projects using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort App projects use the [find_app_projects](toloka.client.TolokaClient.find_app_projects.md) method.

        Example:
            >>> app_projects = toloka_client.get_app_projects(scope='MY')
            >>> for app_project in app_projects:
            >>>     print(app_project.id, app_project.status, app_project.name)
            ...

        Args:
            request: Search criteria.
            batch_size: Returned projects limit for each request. The maximum batch_size is 5000.

        Yields:
            AppProject: The next matching App project.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        generator = self._find_all(self.find_app_projects, request, items_field='content', batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def create_app_project(self, app_project: AppProject) -> AppProject:
        """Creates an App project in Toloka.

        Example:
            >>> app_project = toloka.AppProject(
            >>>   app_id='9lZaMl363jahzra1rrYq',
            >>>   name='Example project (product relevance)',
            >>>   parameters={
            >>>     "default_language": "en",
            >>>     "name": "Product relevance project",
            >>>     "instruction_classes": [
            >>>       {
            >>>         "description": "The product is relevant to the query.",
            >>>         "label": "Relevant",
            >>>         "value": "relevant"
            >>>       },
            >>>       {
            >>>         "description": "The product is not completely relevant to the query.",
            >>>         "label": "Irrelevant",
            >>>         "value": "irrelevant"
            >>>       }
            >>>     ],
            >>>     "instruction_examples": [
            >>>       {
            >>>         "description": "The product exactly matches the query.",
            >>>         "label": "relevant",
            >>>         "query": "some search query",
            >>>         "screenshot_url": "https://example.com/1"
            >>>       },
            >>>       {
            >>>         "description": "The product shape matches but the product color does not.",
            >>>         "label": "irrelevant",
            >>>         "query": "other search query",
            >>>         "screenshot_url": "https://example.com/2"
            >>>       }
            >>>     ]
            >>>   }
            >>> )
            >>> app_project = toloka_client.create_app_project(app_project)
            >>> print(app_project.created, app_project.status)
            ...

        Args:
            app_project: The project with parameters.

        Returns:
            AppProject: Created App project with updated parameters.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        response = self._request('post', '/app/v0/app-projects', json=unstructure(app_project))
        return structure(response, AppProject)

    @add_headers('client')
    def get_app_project(self, app_project_id: str) -> AppProject:
        """Gets information from Toloka about an App project.

        Example:
            >>> app_project = toloka_client.get_app_project('Q2d15QBjpwWuDz8Z321g')
            >>> print(app_project.created, app_project.name)
            ...

        Args:
            app_project_id: The ID of the project.

        Returns:
            AppProject: The App project.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        response = self._request('get', f'/app/v0/app-projects/{app_project_id}')
        return structure(response, AppProject)

    @add_headers('client')
    def archive_app_project(self, app_project_id: str) -> AppProject:
        """Archives an App project.

        The project changes its status to `ARCHIVED`.

        Example:
            >>> toloka_client.archive_app_project('Q2d15QBjpwWuDz8Z321g')
            ...

        Args:
            app_project_id: The ID of the project.

        Returns:
            AppProject: The App project with updated status.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        self._raw_request('post', f'/app/v0/app-projects/{app_project_id}/archive')
        return self.get_app_project(app_project_id)

    @add_headers('client')
    def unarchive_app_project(self, app_project_id: str) -> AppProject:
        """Unarchives an App project.

        Previous project status, which was before archiving, is restored.

        Example:
            >>> toloka_client.unarchive_app_project('Q2d15QBjpwWuDz8Z321g')
            ...

        Args:
            app_project_id: The ID of the project.

        Returns:
            AppProject: The App project with updated status.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        self._raw_request('post', f'/app/v0/app-projects/{app_project_id}/unarchive')
        return self.get_app_project(app_project_id)

    @expand('request')
    @add_headers('client')
    def find_apps(
        self,
        request: search_requests.AppSearchRequest, sort: Union[List[str], search_requests.AppSortItems, None] = None,
        limit: Optional[int] = None
    ) -> search_results.AppSearchResult:
        """Finds App solutions that match certain criteria.

        The number of returned solutions is limited. To find remaining solutions call `find_apps` with updated search criteria.

        To iterate over all matching solutions you may use the [get_apps](toloka.client.TolokaClient.get_apps.md) method.

        Example:
            >>> search = toloka_client.find_apps()
            >>> for app in search.content:
            >>>     print(app.id, app.name)
            >>>
            >>> if search.has_more:
            >>>     print('There are more App solutions...')
            ...

        Args:
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned solutions limit. The maximum allowed limit is 1000.

        Returns:
            AppSearchResult: Found solutions and a flag showing whether there are more matching solutions exceeding the limit.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        sort = None if sort is None else structure(sort, search_requests.AppSortItems)
        response = self._search_request('get', '/app/v0/apps', request, sort, limit)
        return structure(response, search_results.AppSearchResult)

    @expand('request')
    @add_headers('client')
    def get_apps(
        self,
        request: search_requests.AppSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[App, None, None]:
        """Finds all App solutions that match certain criteria.

        `get_apps` returns a generator. You can iterate over all found solutions using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort solutions use the [find_apps](toloka.client.TolokaClient.find_apps.md) method.

        Example:
            >>> apps = toloka_client.get_apps()
            >>> for app in apps:
            >>>     print(app.id, app.name)
            ...

        Args:
            request: Search criteria.
            batch_size: Returned solutions limit for each request. The maximum allowed batch_size is 1000.

        Yields:
            App: The next matching solution.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        generator = self._find_all(self.find_apps, request, items_field='content', batch_size=batch_size)
        yield from generator

    @add_headers('client')
    def get_app(self, app_id: str, lang: Optional[str] = None) -> App:
        """Gets information from Toloka about an App solution.

        Example:
            >>> app = toloka_client.get_app('2eN4l59qL2xHB5b8Jqp6')
            >>> print(app.id, app.name)
            >>> print(app.description)
            ...

        Args:
            app_id: The ID of the solution.
            lang: ISO 639 language code.

        Returns:
            App: The App solution.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        response = self._request('get', f'/app/v0/apps/{app_id}', params={'lang': lang})
        return structure(response, App)

    @expand('request')
    @add_headers('client')
    def find_app_items(
        self,
        app_project_id: str, request: search_requests.AppItemSearchRequest,
        sort: Union[List[str], search_requests.AppItemSortItems, None] = None, limit: Optional[int] = None
    ) -> search_results.AppItemSearchResult:
        """Finds task items that match certain criteria in an App project.

        The number of returned items is limited. To find remaining items call `find_app_items` with updated search criteria.

        To iterate over all matching items you may use the [get_app_items](toloka.client.TolokaClient.get_app_items.md) method.

        Example:
            Finding items in an App project that were created starting some date.
            >>> search = toloka_client.find_app_items(
            >>>     app_project_id = 'Q2d15QBjpwWuDz8Z321g',
            >>>     created_gte = '2022-06-16',
            >>>     sort = 'created')
            >>> for app_item in search.content:
            >>>     print(app_item.id, app_item.created_at)
            >>>
            >>> if search.has_more:
            >>>     print('...')
            ...

        Args:
            app_project_id: The ID of the App project.
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned items limit. The maximum allowed limit is 1000.

        Returns:
            AppItemSearchResult: Found task items and a flag showing whether there are more matching items exceeding the limit.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        sort = None if sort is None else structure(sort, search_requests.AppItemSortItems)
        response = self._search_request('get', f'/app/v0/app-projects/{app_project_id}/items', request, sort, limit)
        return structure(response, search_results.AppItemSearchResult)

    @expand('request')
    @add_headers('client')
    def get_app_items(
        self,
        app_project_id: str, request: search_requests.AppItemSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[AppItem, None, None]:
        """Finds all App task items that match certain criteria in an App project.

        `get_app_items` returns a generator. You can iterate over all found items using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort items use the [find_app_items](toloka.client.TolokaClient.find_app_items.md) method.

        Example:
            >>> items = toloka_client.get_app_items('Q2d15QBjpwWuDz8Z321g')
            >>> for item in items:
            >>>     print(item.id, item.status, item.finished_at)
            ...

        Args:
            app_project_id: The ID of the App project.
            request: Search criteria.
            batch_size: Returned items limit for each request. The maximum allowed batch_size is 1000.

        Yields:
            AppItem: The next matching item.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        find_function = functools.partial(self.find_app_items, app_project_id)
        generator = self._find_all(find_function, request, items_field='content', batch_size=batch_size)
        yield from generator

    @expand('app_item')
    @add_headers('client')
    def create_app_item(self, app_project_id: str, app_item: AppItem) -> AppItem:
        """Creates an App task item in Toloka.

        Example:
            The following example is suitable for a project
            that requires `query` and `website_url` keys to be present in input data.

            >>> new_item = {
            >>>     'batch_id' : '4Va2BBWKL88S4QyAgVje',
            >>>     'input_data' : {
            >>>         'id':'40', 'query':'toloka kit', 'website_url':'https://toloka.ai/docs/toloka-kit'
            >>>     }
            >>> }
            >>> new_item = toloka_client.create_app_item(app_project_id = 'Q2d15QBjpwWuDz8Z321g', app_item = new_item)
            >>> print(new_item.created_at)
            ...

        Args:
            app_project_id: The ID of the App project to create the item in.
            app_item: The task item with parameters.

        Returns:
            AppItem: Created App task item with updated parameters.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        response = self._request('post', f'/app/v0/app-projects/{app_project_id}/items', json=unstructure(app_item))
        return structure(response, AppItem)

    @expand('request')
    @add_headers('client')
    def create_app_items(self, app_project_id: str, request: AppItemsCreateRequest):
        """Creates task items in an App project in Toloka and adds them to an existing batch.

        Example:
            The following example is suitable for a project
            that requires `query` and `website_url` keys to be present in input data.

            >>> new_items = [
            >>>     {'id':'20', 'query':'toloka kit', 'website_url':'https://toloka.ai/docs/toloka-kit'},
            >>>     {'id':'21', 'query':'crowd kit', 'website_url':'https://toloka.ai/docs/crowd-kit'}
            >>> ]
            >>> toloka_client.create_app_items(app_project_id = 'Q2d15QBjpwWuDz8Z321g', batch_id = '4Va2BBWKL88S4QyAgVje', items = new_items)
            ...

        Args:
            app_project_id: The ID of the App project.
            request: The request parameters.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        self._raw_request('post', f'/app/v0/app-projects/{app_project_id}/items/bulk', json=unstructure(request))
        return

    @add_headers('client')
    def get_app_item(self, app_project_id: str, app_item_id: str) -> AppItem:
        """Gets information from Toloka about an App task item.

        Example:
            >>> item = toloka_client.get_app_item(app_project_id = 'Q2d15QBjpwWuDz8Z321g', app_item_id = 'V40aPPA2j64TORQyY54Z')
            >>> print(item.input_data)
            >>> print(item.output_data)
            ...

        Args:
            app_project_id: The ID of the App project.
            app_item_id: The ID of the item.

        Returns:
            AppItem: The App task item.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        response = self._request('get', f'/app/v0/app-projects/{app_project_id}/items/{app_item_id}')
        return structure(response, AppItem)

    @expand('request')
    @add_headers('client')
    def find_app_batches(self, app_project_id: str,
                         request: search_requests.AppBatchSearchRequest,
                         sort: Union[List[str], search_requests.AppBatchSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.AppBatchSearchResult:
        """Finds batches that match certain criteria in an App project.

        The number of returned batches is limited. To find remaining batches call `find_app_batches` with updated search criteria.

        To iterate over all matching batches you may use the [get_app_batches](toloka.client.TolokaClient.get_app_batches.md) method.

        Args:
            app_project_id: The ID of the App project.
            request: Search criteria.
            sort: Sorting options. Default: `None`.
            limit: Returned batches limit. The maximum allowed limit is 1000.

        Returns:
            AppBatchSearchResult: Found batches and a flag showing whether there are more matching batches exceeding the limit.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        sort = None if sort is None else structure(sort, search_requests.AppBatchSortItems)
        response = self._search_request('get', f'/app/v0/app-projects/{app_project_id}/batches', request, sort, limit)
        return structure(response, search_results.AppBatchSearchResult)

    @expand('request')
    @add_headers('client')
    def get_app_batches(
        self,
        app_project_id: str,
        request: search_requests.AppBatchSearchRequest,
        batch_size: Optional[int] = None
    ) -> Generator[AppBatch, None, None]:
        """Finds all batches that match certain criteria in an App project.

        `get_app_batches` returns a generator. You can iterate over all found batches using the generator. Several requests to the Toloka server are possible while iterating.

        If you need to sort batches use the [find_app_batches](toloka.client.TolokaClient.find_app_batches.md) method.

        Example:
            >>> batches = toloka_client.get_app_batches(app_project_id = 'Q2d15QBjpwWuDz8Z321g', status = 'NEW')
            >>> for batch in batches:
            >>>     print(batch.id, batch.status, batch.items_count)
            ...

        Args:
            app_project_id: The ID of the App project.
            request: Search criteria.
            batch_size: Returned app batches limit for each request. The maximum allowed batch_size is 1000.

        Yields:
            AppBatch: The next matching batch.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        find_function = functools.partial(self.find_app_batches, app_project_id)
        generator = self._find_all(find_function, request, items_field='content', batch_size=batch_size)
        yield from generator

    @expand('request')
    @add_headers('client')
    def create_app_batch(self, app_project_id: str, request: AppBatchCreateRequest) -> AppBatch:
        """Creates a batch with task items in an App project in Toloka.

        Example:
            The following example is suitable for a project
            that requires `query` and `website_url` keys to be present in input data.

            >>> new_items = [
            >>>     {'id':'30', 'query':'toloka kit', 'website_url':'https://toloka.ai/docs/toloka-kit'},
            >>>     {'id':'31', 'query':'crowd kit', 'website_url':'https://toloka.ai/docs/crowd-kit'}
            >>> ]
            >>> toloka_client.create_app_batch(app_project_id = 'Q2d15QBjpwWuDz8Z321g', items = new_items)
            ...

        Args:
            app_project_id: The ID of the project.
            request: The request parameters.

        Returns:
            AppBatch: Created batch with updated parameters.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        response = self._request('post', f'/app/v0/app-projects/{app_project_id}/batches', json=unstructure(request))
        return structure(response, AppBatch)

    @add_headers('client')
    def get_app_batch(self, app_project_id: str, batch_id: str) -> AppBatch:
        """Gets information from Toloka about a batch in an App project.

        Example:
            >>> batch = toloka_client.get_app_batch(app_project_id = 'Q2d15QBjpwWuDz8Z321g', app_batch_id = '4Va2BBWKL88S4QyAgVje')
            >>> print(batch.status, batch.items_count, batch.cost)
            ...

        Args:
            app_project_id: The ID of the project.
            batch_id: The ID of the batch.

        Returns:
            AppBatch: The App batch.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        response = self._request('get', f'/app/v0/app-projects/{app_project_id}/batches/{batch_id}')
        return structure(response, AppBatch)

    @expand('patch')
    @add_headers('client')
    def patch_app_batch(self, app_project_id: str, batch_id: str, patch: AppBatchPatch) -> AppBatch:
        """Updates an App batch.

        Args:
            app_project_id: The ID of the App project containing the batch.
            batch_id: The ID of the batch.
            patch: Parameters to update.

        Example:
            Changing the batch name.

            >>> batch = toloka_client.patch_app_batch(
            >>>     app_project_id = 'Q2d15QBjpwWuDz8Z321g', batch_id = '4Va2BBWKL88S4QyAgVje',
            >>>     name = 'Preliminary batch')
            ...

        Returns:
            AppBatch: The updated App batch.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        response = self._request(
            'patch', f'/app/v0/app-projects/{app_project_id}/batches/{batch_id}', json=unstructure(patch)
        )
        return structure(response, AppBatch)

    @add_headers('client')
    def start_app_batch(self, app_project_id: str, batch_id: str):
        """Launches annotation of a batch of task items in an App project.

        Example:
            >>> toloka_client.start_app_batch(app_project_id = 'Q2d15QBjpwWuDz8Z321g', app_batch_id = '4Va2BBWKL88S4QyAgVje')
            ...

        Args:
            app_project_id: The ID of the project.
            batch_id: The ID of the batch.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        self._raw_request('post', f'/app/v0/app-projects/{app_project_id}/batches/{batch_id}/start')
        return

    @add_headers('client')
    def stop_app_batch(self, app_project_id: str, batch_id: str):
        """Stops annotation of a batch of task items in an App project.

        Processing can be stopped only for the batch with the `PROCESSING` status.

        Example:
            >>> toloka_client.stop_app_batch(app_project_id = 'Q2d15QBjpwWuDz8Z321g', batch_id = '4Va2BBWKL88S4QyAgVje')
            ...

        Args:
            app_project_id: The ID of the project.
            batch_id: The ID of the batch.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        self._raw_request('post', f'/app/v0/app-projects/{app_project_id}/batches/{batch_id}/stop')
        return

    @add_headers('client')
    def resume_app_batch(self, app_project_id: str, batch_id: str):
        """Resumes annotation of a batch of task items in an App project.

        Processing can be resumed only for the batch with the `STOPPING` or `STOPPED` status.

        Example:
            >>> toloka_client.resume_app_batch(app_project_id = 'Q2d15QBjpwWuDz8Z321g', batch_id = '4Va2BBWKL88S4QyAgVje')
            ...

        Args:
            app_project_id: The ID of the project.
            batch_id: The ID of the batch.
        """

        if self.url != self.Environment.PRODUCTION.value:
            raise RuntimeError('this method supports only production environment')

        self._raw_request('post', f'/app/v0/app-projects/{app_project_id}/batches/{batch_id}/resume')
        return
