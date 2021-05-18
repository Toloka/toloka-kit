__all__ = [
    'TolokaClient',
    'Assignment',
    'Attachment',
    'Folder',
    'MessageThread',
    'MessageThreadReply',
    'MessageThreadFolders',
    'MessageThreadCompose',
    'Skill',
    'TaskSuite',
    'Task',
    'Training',
    'UserBonus',
    'Pool',
    'Project',
]
import datetime
from decimal import Decimal
import time
from enum import Enum, unique
from typing import List, Optional, Union, BinaryIO, Tuple, Generator
import pandas as pd

import attr

import io
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import uuid

from . import actions  # noqa: F401
from . import aggregation
from . import batch_create_results
from . import collectors  # noqa: F401
from . import conditions  # noqa: F401
from . import operations
from . import search_requests
from . import search_results
from . import task
from . import task_suite
from .__version__ import __version__
from ._converter import structure, unstructure
from .aggregation import AggregatedSolution
from .analytics_request import AnalyticsRequest
from .assignment import Assignment, AssignmentPatch, GetAssignmentsTsvParameters
from .attachment import Attachment
from .clone_results import CloneResults
from .exceptions import raise_on_api_error, ValidationApiError
from .message_thread import (
    Folder, MessageThread, MessageThreadReply, MessageThreadFolders, MessageThreadCompose
)
from .operation_log import OperationLogItem
from .pool import Pool, PoolPatchRequest
from .project import Project
from .training import Training
from .requester import Requester
from .skill import Skill
from .task import Task
from .task_suite import TaskSuite
from .user_bonus import UserBonus, UserBonusCreateRequestParameters
from .user_restriction import UserRestriction
from .user_skill import SetUserSkillRequest, UserSkill
from .util._codegen import expand

logger = logging.getLogger(__name__)


class TolokaClient:
    """Implements interaction with the Toloka API

    All other objects are created or modified only in the memory of your computer.
    Only by calling one of the TolokaClient methods, you can transfer information from these objects to Toloka.
    For Example. If you create an instance of Project, it will not create such a project in Toloka. You need to call the
    TolokaClient.create_project method and pass the project instance there.
    Likewise. If you read the project using the TolokaClient.get_project method, you will get an instance of Project.
    But if you change something in this object, it will not affect the existing project in Toloka. To apply these changes,
    call TolokaClient.update_project and pass the changed Project there.

    Args:
        token: You OAuth token for Toloka. You can learn more about how to get it here: https://yandex.ru/dev/toloka/doc/concepts/access.html?lang=en
        environment: There are two versions of Toloka. You need to register separately in each of them:
            * SANDBOX: Testing version oif Toloka. You can test complex projects before the start. Nobody saw your tasks.
            * PRODUCTION: Production version of Toloka for requesters. You spend money and get result.
        retries: Retry policy. You can use the following types:
            * int - The number of retries for all requests. In this case, the retry policy is created automatically.
            * Retry - Fully specified retry policy that will apply to all requests.
        timeout: Same as timeout in Requests. The connect timeout is the number of seconds Requests will wait for your client
            to establish a connection to a remote machine call on the socket.
            * If you specify a single value for the timeout, it will be applied to both the connect and the read timeouts.
            * Specify a tuple if you would like to set the values separately.
            * Set the timeout value to None if you're willing to wait forever.
        url: If you want to set a specific URL for some reason, for example, for testing.
            You can only set one parameter, "url" or "environment", not both.

    Example:
        How to create TolokaClient and make you first request to Toloka.

        >>> import toloka.client as toloka
        >>> token = input("Enter your token:")
        >>> toloka_client = toloka.TolokaClient(token, 'PRODUCTION')
        >>> print(toloka_client.get_requester())
        ...
    """

    @unique
    class Environment(Enum):
        SANDBOX = 'https://sandbox.toloka.yandex.com'
        PRODUCTION = 'https://toloka.yandex.com'

    def __init__(
        self,
        token: str,
        environment: Union[Environment, str, None] = None,
        retries: Union[int, Retry] = 3,
        timeout: Union[float, Tuple[float, float]] = 10.0,
        url: Optional[str] = None
    ):
        if url is None and environment is None:
            raise ValueError('You must pass at least one parameter: url or environment.')
        if url is not None and environment is not None:
            raise ValueError('You can only pass one parameter: environment or url. Both are now set.')
        if url is not None:
            self.url = url[:-1] if url.endswith('/') else url
        else:
            if not isinstance(environment, TolokaClient.Environment):
                environment = TolokaClient.Environment[environment.upper()]
            self.url = environment.value
        self.token = token
        status_list = [status_code for status_code in requests.status_codes._codes if status_code > 405]
        if not isinstance(retries, Retry):
            retries = Retry(
                total=retries,
                status_forcelist=status_list,
                method_whitelist=['HEAD', 'GET', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'POST', 'PATCH'],
                backoff_factor=2,  # summary retry time more than 10 seconds
            )
        adapter = HTTPAdapter(max_retries=retries)
        self.session = requests.Session()
        self.session.mount(self.url, adapter)

        self.session.headers.update(
            {
                'Authorization': f'OAuth {self.token}',
                'User-Agent': f'python-toloka-client-{__version__}',
            }
        )
        # float, or a (connect timeout, read timeout) tuple
        # How long to wait for the server to send data before giving up,
        # If None - wait forever for a response/
        self.default_timeout = timeout

    def _raw_request(self, method, path, **kwargs):

        # Fixing capitalisation in boolean parameters
        if kwargs.get('params'):
            params = kwargs['params']
            for key, value in params.items():
                if isinstance(value, bool):
                    params[key] = 'true' if value else 'false'
        if self.default_timeout is not None and 'timeout' not in kwargs:
            kwargs['timeout'] = self.default_timeout
        response = self.session.request(method, f'{self.url}/api{path}', **kwargs)
        raise_on_api_error(response)
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

    def _find_all(self, find_function, request):
        result = find_function(request, sort=['id'])
        while result.has_more:
            request = attr.evolve(request, id_gt=result.items[-1].id)
            yield from result.items
            result = find_function(request, sort=['id'])

        yield from result.items

    def _sync_via_async(self, objects, parameters, url, result_type, operation_type, output_id_field, get_method):
        if not parameters.async_mode:
            response = self._request('post', url, json=unstructure(objects), params=unstructure(parameters))
            return structure(response, result_type)

        # Emulates synchronous operation, through asynchronous calls and reading operation logs.
        client_uuid_to_index = {}
        for i, obj in enumerate(objects):
            obj._unexpected['__client_uuid'] = uuid.uuid4().hex
            client_uuid_to_index[obj._unexpected['__client_uuid']] = str(i)

        response = self._request('post', url, json=unstructure(objects), params=unstructure(parameters))
        insert_operation = structure(response, operation_type)
        insert_operation = self.wait_operation(insert_operation, datetime.timedelta(minutes=60))

        pools = {}
        validation_errors = {}

        for log_item in self.get_operation_log(insert_operation.id):
            if log_item.type not in ['TASK_CREATE', 'TASK_VALIDATE', 'TASK_SUITE_VALIDATE', 'TASK_SUITE_CREATE']:
                continue
            if '__client_uuid' in log_item.input and log_item.input['__client_uuid'] in client_uuid_to_index:
                index = client_uuid_to_index[log_item.input['__client_uuid']]
            else:
                continue
            if log_item.success:
                numerated_ids = pools.setdefault(log_item.input['pool_id'], {})
                numerated_ids[log_item.output[output_id_field]] = index
            else:
                validation_errors[index] = {
                    name: structure(error, batch_create_results.FieldValidationError)
                    for name, error in log_item.output.items()
                }

        # Emulates the response as in a synchronous method:
        # it will throw an exception even if the skip_invalid_items parameter is passed
        # but no objects are created
        if not pools:
            raise ValidationApiError(
                code='VALIDATION_ERROR',
                message='Validation failed',
                payload=validation_errors
            )

        # get object from all pools
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

        return result_type(items=items, validation_errors=validation_errors or {})

    # Aggregation section

    @expand('request')
    def aggregate_solutions_by_pool(self, request: aggregation.PoolAggregatedSolutionRequest) -> operations.AggregatedSolutionOperation:
        """Starts aggregation of solutions in the pool

        Responses to all completed tasks will be aggregated.
        The method only starts the aggregation and returns the operation for further tracking.

        Note: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
        methods and can perform on your computers: https://github.com/Toloka/crowd-kit

        Args:
            request: Parameters describing in which pool to aggregate solutions and by what rules.

        Returns:
            operations.AggregatedSolutionOperation: An operation upon completion of which you can get the results of the aggregation.

        Example:
            How to start aggregating solutions by pool.

            >>> aggregation_operation = toloka_client.aggregate_solutions_by_pool(
            >>>         type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
            >>>         pool_id=some_existing_pool_id,   # Aggregate in this pool
            >>>         answer_weight_skill_id=some_skill_id,   # Aggregate by this skill
            >>>         fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]  # Aggregate this field
            >>>     )
            >>> aggregation_operation = toloka_client.wait_operation(aggregation_operation)
            >>> # Now you can call "find_aggregated_solutions"
            ...
        """
        data = unstructure(request)
        response = self._request('post', '/v1/aggregated-solutions/aggregate-by-pool', json=data)
        return structure(response, operations.AggregatedSolutionOperation)

    @expand('request')
    def aggregate_solutions_by_task(self, request: aggregation.WeightedDynamicOverlapTaskAggregatedSolutionRequest) -> AggregatedSolution:
        """Starts aggregation of solutions to a single task

        The method only starts the aggregation and returns the operation for further tracking.

        Args:
            request: Parameters describing on which task to aggregate solutions and by what rules.

        Returns:
            AggregatedSolution: Result of aggregation. Also contains input parameters and result confidence.

        Example:
            How to aggregate solutions to a task.

            >>> aggregation_operation = toloka_client.aggregate_solutions_by_task(
            >>>         type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
            >>>         pool_id=some_existing_pool_id,   # Task in this pool
            >>>         task_id=some_existing_task_id,   # Aggregate on this task
            >>>         answer_weight_skill_id=some_skill_id,   # Aggregate by this skill
            >>>         fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]  # Aggregate this field
            >>>     )
            >>> print(aggregation_operation.output_values['result'])
            ...
        """
        response = self._request('post', '/v1/aggregated-solutions/aggregate-by-task', json=unstructure(request))
        return structure(response, AggregatedSolution)

    @expand('request')
    def find_aggregated_solutions(self, operation_id: str, request: search_requests.AggregatedSolutionSearchRequest,
                                  sort: Union[List[str], search_requests.AggregatedSolutionSortItems, None] = None,
                                  limit: Optional[int] = None) -> search_results.AggregatedSolutionSearchResult:
        """Gets aggregated responses after the AggregatedSolutionOperation completes

        Note: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
        methods and can perform on your computers: https://github.com/Toloka/crowd-kit

        Args:
            operation_id: From what aggregation operation you want to get results.
            request: How to filter search results.
            sort: How to sort results. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AggregatedSolutionSearchResult: The first "limit" solutions in "items". And a mark that there is more.

        Example:
            How to get all aggregated solutions from pool.

            >>> # run toloka_client.aggregate_solutions_by_pool and wait operation for closing.
            >>> current_result = toloka_client.find_aggregated_solutions(aggregation_operation.id)
            >>> aggregation_results = current_result.items
            >>> # If we have more results, let's get them
            >>> while current_result.has_more:
            >>>     current_result = toloka_client.find_aggregated_solutions(
            >>>         aggregation_operation.id,
            >>>         task_id_gt=current_result.items[len(current_result.items) - 1].task_id,
            >>>     )
            >>>     aggregation_results = aggregation_results + current_result.items
            >>> print(len(aggregation_results))
            ...
        """
        sort = None if sort is None else structure(sort, search_requests.AggregatedSolutionSortItems)
        response = self._search_request('get', f'/v1/aggregated-solutions/{operation_id}', request, sort, limit)
        return structure(response, search_results.AggregatedSolutionSearchResult)

    # Assignments section

    def accept_assignment(self, assignment_id: str, public_comment: str) -> Assignment:
        """Marks one assignment as accepted

        Used then your pool created with auto_accept_solutions=False parametr.

        Args:
            assignment_id: What assignment will be accepted.
            public_comment: Message to the performer.

        Returns:
            Assignment: Object with new status.

        Example:
            How to accept one assignment.

            >>> toloka_client.accept_assignment(assignment_id, "Well done!")
        """
        return self.patch_assignment(assignment_id, public_comment=public_comment, status=Assignment.ACCEPTED)

    @expand('request')
    def find_assignments(self, request: search_requests.AssignmentSearchRequest,
                         sort: Union[List[str], search_requests.AssignmentSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.AssignmentSearchResult:
        """Finds all assignments that match certain rules

        As a result, it returns an object that contains the first part of the found assignments and whether there
        are any more results.
        It is better to use the "get_assignments" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search assignments.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of assignments returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AssignmentSearchResult: The first "limit" assignments in "items". And a mark that there is more.

        """
        sort = None if sort is None else structure(sort, search_requests.AssignmentSortItems)
        response = self._search_request('get', '/v1/assignments', request, sort, limit)
        return structure(response, search_results.AssignmentSearchResult)

    def get_assignment(self, assignment_id: str) -> Assignment:
        """Reads one specific assignment

        Args:
            assignment_id: ID of assignment.

        Returns:
            Assignment: The solution read as a result.
        """
        response = self._request('get', f'/v1/assignments/{assignment_id}')
        return structure(response, Assignment)

    @expand('request')
    def get_assignments(self, request: search_requests.AssignmentSearchRequest) -> Generator[Assignment, None, None]:
        """Finds all assignments that match certain rules and returns them in an iterable object

        Unlike find_assignments, returns generator. Does not sort assignments.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search assignments.

        Yields:
            Assignment: The next object corresponding to the request parameters.

        Example:
            How to process all accepted assignmens.

            >>> for assignment in toloka_client.get_assignments(pool_id=some_pool_id, status=['ACCEPTED', 'SUBMITTED']):
            >>>     # somehow process "assignment"
            ...
        """
        return self._find_all(self.find_assignments, request)

    @expand('patch')
    def patch_assignment(self, assignment_id: str, patch: AssignmentPatch) -> Assignment:
        """Changes status and comment on assignment

        It's better to use methods "reject_assignment" and "accept_assignment".

        Args:
            assignment_id: What assignment will be affected.
            patch: Object with new status and comment.

        Returns:
            Assignment: Object with new status.
        """
        response = self._request('patch', f'/v1/assignments/{assignment_id}', json=unstructure(patch))
        return structure(response, Assignment)

    def reject_assignment(self, assignment_id: str, public_comment: str) -> Assignment:
        """Marks one assignment as rejected

        Used then your pool created with auto_accept_solutions=False parametr.

        Args:
            assignment_id: What assignment will be rejected.
            public_comment: Message to the performer.

        Returns:
            Assignment: Object with new status.

        Example:
            How to reject one assignment.

            >>> toloka_client.reject_assignment(assignment_id, "Bad work.")
        """
        return self.patch_assignment(assignment_id, public_comment=public_comment, status=Assignment.REJECTED)

    # Attachment section

    @expand('request')
    def find_attachments(self, request: search_requests.AttachmentSearchRequest,
                         sort: Union[List[str], search_requests.AttachmentSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.AttachmentSearchResult:
        """Finds all attachments that match certain rules

        As a result, it returns an object that contains the first part of the found attachments and whether there
        are any more results.
        It is better to use the "get_attachments" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search attachments.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100,000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.AttachmentSearchResult: The first "limit" assignments in "items". And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.AttachmentSortItems)
        response = self._search_request('get', '/v1/attachments', request, sort, limit)
        return structure(response, search_results.AttachmentSearchResult)

    def get_attachment(self, attachment_id: str) -> Attachment:
        """Gets attachment metadata without downloading it

        To download attachments as a file use "TolokaClient.download_attachment" method.

        Args:
            attachment_id: ID of attachment.

        Returns:
            Attachment: The attachment metadata read as a result.
        """
        response = self._request('get', f'/v1/attachments/{attachment_id}')
        return structure(response, Attachment)

    @expand('request')
    def get_attachments(self, request: search_requests.AttachmentSearchRequest) -> Generator[Attachment, None, None]:
        """Finds all attachments that match certain rules and returns their metadata in an iterable object

        Unlike find_attachments, returns generator. Does not sort attachments.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search attachments.

        Yields:
            Attachment: The next object corresponding to the request parameters.
        """
        return self._find_all(self.find_attachments, request)

    def download_attachment(self, attachment_id: str, out: BinaryIO) -> None:
        """Downloads specific attachment

        Args:
            attachment_id: ID of attachment.
            out: File object where to put downloaded file.

        Example:
            How to download attachment.

            >>> with open('my_new_file.txt', 'wb') as out_f:
            >>>     toloka_client.download_attachment('attachment-id', out_f)
            ...
        """
        response = self._raw_request('get', f'/v1/attachments/{attachment_id}/download', stream=True)
        for content in response.iter_content():
            out.write(content)

    # Message section

    def add_message_thread_to_folders(self, message_thread_id: str, folders: Union[List[Folder], MessageThreadFolders]) -> MessageThread:
        """Adds a message chain to one or more folders ("unread", "important" etc.)

        Args:
            message_thread_id: ID of message chain.
            folders: List of folders, where to move chain.

        Returns:
            MessageThread: Full object by ID with updated folders.
        """
        if not isinstance(folders, MessageThreadFolders):
            folders = structure({'folders': folders}, MessageThreadFolders)
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/add-to-folders', json=unstructure(folders))
        return structure(response, MessageThread)

    @expand('compose')
    def compose_message_thread(self, compose: MessageThreadCompose) -> MessageThread:
        """Sends message to performer

        The sent message is added to a new message thread.

        Args:
            compose: Message parameters.

        Returns:
            MessageThread: New created thread.
        """
        response = self._request('post', '/v1/message-threads/compose', json=unstructure(compose))
        return structure(response, MessageThread)

    @expand('request')
    def find_message_threads(self, request: search_requests.MessageThreadSearchRequest,
                             sort: Union[List[str], search_requests.MessageThreadSortItems, None] = None,
                             limit: Optional[int] = None) -> search_results.MessageThreadSearchResult:
        """Finds all message threads that match certain rules

        As a result, it returns an object that contains the first part of the found threads and whether there
        are any more results.
        It is better to use the "get_message_threads" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request:  How to search threads.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            search_results.MessageThreadSearchResult: The first "limit" message threads in "items".
                And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.MessageThreadSortItems)
        response = self._search_request('get', '/v1/message-threads', request, sort, limit)
        return structure(response, search_results.MessageThreadSearchResult)

    def reply_message_thread(self, message_thread_id: str, reply: MessageThreadReply) -> MessageThread:
        """Replies to a message in thread

        Args:
            message_thread_id: In which thread to reply.
            reply: Reply message.

        Returns:
            MessageThread: New created message.
        """
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/reply', json=unstructure(reply))
        return structure(response, MessageThread)

    @expand('request')
    def get_message_threads(self, request: search_requests.MessageThreadSearchRequest) -> Generator[MessageThread, None, None]:
        """Finds all message threads that match certain rules and returns them in an iterable object

        Unlike find_message_threads, returns generator. Does not sort threads.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search attachments.

        Yields:
            MessageThread: The next object corresponding to the request parameters.

        Example:
            How to get all unread incoming messages.

            >>> message_threads = toloka_client.get_message_threads(folder=['INBOX', 'UNREAD'])
            ...
        """
        return self._find_all(self.find_message_threads, request)

    def remove_message_thread_from_folders(self, message_thread_id: str, folders: Union[List[Folder], MessageThreadFolders]) -> MessageThread:
        """Deletes a message chain from one or more folders ("unread", "important" etc.)

        Args:
            message_thread_id: ID of message chain.
            folders:  List of folders, where from to remove chain.

        Returns:
            MessageThread: Full object by ID with updated folders.
        """
        if not isinstance(folders, MessageThreadFolders):
            folders = structure({'folders': folders}, MessageThreadFolders)
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/remove-from-folders', json=unstructure(folders))
        return structure(response, MessageThread)

    # Project section

    def archive_project(self, project_id: str) -> Project:
        """Sends project to archive

        Use it when you have no need this project anymore. To perform the operation, all pools in the project must be archived.
        The archived project is not deleted. You can access it when you will need it.

        Args:
            project_id: ID of project that will be archived.

        Returns:
            Project: Object with updated status.
        """
        operation = self.archive_project_async(project_id)
        operation = self.wait_operation(operation)
        return self.get_project(operation.parameters.project_id)

    def archive_project_async(self, project_id: str) -> operations.ProjectArchiveOperation:
        """Sends project to archive, asynchronous version

        Use when you have no need this project anymore. To perform the operation, all pools in the project must be archived.
        The archived project is not deleted. You can access it when you will need it.

        Args:
            project_id: ID of project that will be archived.

        Returns:
            ProjectArchiveOperation: An operation upon completion of which you can get the project with updated status.
        """
        response = self._request('post', f'/v1/projects/{project_id}/archive')
        return structure(response, operations.ProjectArchiveOperation)

    def create_project(self, project: Project) -> Project:
        """Creates a new project

        Args:
            project: New Project with setted parameters.

        Returns:
            Project: Created project. With read-only fields.

        Example:
            How to create a new project.

            >>> new_project = toloka.project.Project(
            >>>     assignments_issuing_type=toloka.project.Project.AssignmentsIssuingType.AUTOMATED,
            >>>     public_name='My best project',
            >>>     public_description='Describe the picture',
            >>>     public_instructions='Describe in a few words what is happening in the image.',
            >>>     task_spec=toloka.project.task_spec.TaskSpec(
            >>>         input_spec={'image': toloka.project.field_spec.UrlSpec()},
            >>>         output_spec={'result': toloka.project.field_spec.StringSpec()},
            >>>         view_spec=project_interface,
            >>>     ),
            >>> )
            >>> new_project = toloka_client.create_project(new_project)
            >>> print(new_project.id)
            ...
        """
        response = self._request('post', '/v1/projects', json=unstructure(project))
        result = structure(response, Project)
        logger.info(f'A new project with ID "{result.id}" has been created. Link to open in web interface: {self.url}/requester/project/{result.id}')
        return result

    @expand('request')
    def find_projects(self, request: search_requests.ProjectSearchRequest,
                      sort: Union[List[str], search_requests.ProjectSortItems, None] = None,
                      limit: Optional[int] = None) -> search_results.ProjectSearchResult:
        """Finds all projects that match certain rules

        As a result, it returns an object that contains the first part of the found projects and whether there
        are any more results.
        It is better to use the "get_projects" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search projects.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 20 results.

        Returns:
            search_results.ProjectSearchResult: The first "limit" projects in "items".
                And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.ProjectSortItems)
        response = self._search_request('get', '/v1/projects', request, sort, limit)
        return structure(response, search_results.ProjectSearchResult)

    def get_project(self, project_id: str) -> Project:
        """Reads one specific project

        Args:
            project_id: ID of the project.

        Returns:
            Project: The project.
        """
        response = self._request('get', f'/v1/projects/{project_id}')
        return structure(response, Project)

    @expand('request')
    def get_projects(self, request: search_requests.ProjectSearchRequest) -> Generator[Project, None, None]:
        """Finds all projects that match certain rules and returns them in an iterable object

        Unlike find_projects, returns generator. Does not sort projects.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search projects.

        Yields:
            Project: The next object corresponding to the request parameters.

        Example:
            How to get all active projects.

            >>> active_projects = toloka_client.get_projects(status='ACTIVE'):
            ...

            How to get all your projects.

            >>> my_projects = toloka_client.get_projects()
            ...
        """
        return self._find_all(self.find_projects, request)

    def update_project(self, project_id: str, project: Project) -> Project:
        """Makes changes to the project

        Args:
            project_id: Project ID that will be changed.
            project: A project object with all the fields: those that will be updated and those that will not.

        Returns:
            Project: Project object with all fields.
        """
        response = self._request('put', f'/v1/projects/{project_id}', json=unstructure(project))
        return structure(response, Project)

    def clone_project(self, project_id: str, reuse_controllers: bool = True) -> CloneResults:
        """Synchronously clones the project, all pools and trainings

        Emulates cloning behaviour via Toloka interface:
        - the same skills will be used
        - the same quality control collectors will be used (could be changed by reuse_controllers=False)
        - the expiration date will not be changed in the new project
        - etc.

        Doesn't have transaction - can clone project, and then raise on cloning pool.
        Doesn't copy tasks/golden tasks/training tasks.

        Args:
            project_id: ID of the project to be cloned.
            reuse_quality_controllers: Use same quality controllers in cloned and created projects. Defaults to True.
                This means that all quality control rules will be applied to both projects.
                For example, if you have rule "fast_submitted_count", fast responses counts across both projects.

        Returns:
            Tuple[Project, List[Pool], List[Training]]: All created objects project, pools and trainings.

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
        for training in self.get_trainings(project_id=project_id):
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

    def archive_pool(self, pool_id: str) -> Pool:
        """Sends pool to archive

        The pool must be in the status "closed".
        The archived pool is not deleted. You can access it when you will need it.

        Args:
            pool_id: ID of pool that will be archived.

        Returns:
            Pool: Object with updated status.
        """
        operation = self.archive_pool_async(pool_id)
        operation = self.wait_operation(operation)
        return self.get_pool(operation.parameters.pool_id)

    def archive_pool_async(self, pool_id: str) -> operations.PoolArchiveOperation:
        """Sends pool to archive, asynchronous version

        The pool must be in the status "closed".
        The archived pool is not deleted. You can access it when you will need it.

        Args:
            pool_id: ID of pool that will be archived.

        Returns:
            PoolArchiveOperation: An operation upon completion of which you can get the pool with updated status.
        """
        response = self._request('post', f'/v1/pools/{pool_id}/archive')
        return structure(response, operations.PoolArchiveOperation)

    def close_pool(self, pool_id: str) -> Pool:
        """Stops distributing tasks from the pool

        If all tasks done, the pool will be closed automatically.

        Args:
            pool_id: ID of the pool that will be closed.

        Returns:
            Pool: Pool object with new status.
        """
        operation = self.close_pool_async(pool_id)
        operation = self.wait_operation(operation)
        return self.get_pool(operation.parameters.pool_id)

    def close_pool_async(self, pool_id: str) -> operations.PoolCloseOperation:
        """Stops distributing tasks from the pool, asynchronous version

        If all tasks done, the pool will be closed automatically.

        Args:
            pool_id: ID of the pool that will be closed.

        Returns:
            PoolCloseOperation: An operation upon completion of which you can get the pool with updated status.
        """
        response = self._request('post', f'/v1/pools/{pool_id}/close')
        return structure(response, operations.PoolCloseOperation)

    def close_pool_for_update(self, pool_id: str) -> Pool:
        operation = self.close_pool_for_update_async(pool_id)
        operation = self.wait_operation(operation)
        return self.get_pool(operation.parameters.pool_id)

    def close_pool_for_update_async(self, pool_id: str) -> operations.PoolCloseOperation:
        response = self._request('post', f'/v1/pools/{pool_id}/close-for-update')
        return structure(response, operations.PoolCloseOperation)

    def clone_pool(self, pool_id: str) -> Pool:
        """Duplicates existing pool

        An empty pool with the same parameters will be created.
        A new pool will be attached to the same project.

        Args:
            pool_id: ID of the existing pool.

        Returns:
            Pool: New pool.
        """
        operation = self.clone_pool_async(pool_id)
        operation = self.wait_operation(operation)
        result = self.get_pool(operation.details.pool_id)
        logger.info(f'A new pool with ID "{result.id}" has been cloned. Link to open in web interface: {self.url}/requester/project/{result.project_id}/pool/{result.id}')
        return result

    def clone_pool_async(self, pool_id: str) -> operations.PoolCloneOperation:
        """Duplicates existing pool, asynchronous version

        An empty pool with the same parameters will be created.
        A new pool will be attached to the same project.

        Args:
            pool_id: ID of the existing pool.

        Returns:
            PoolCloneOperation: An operation upon completion of which you can get the new pool.
        """
        response = self._request('post', f'/v1/pools/{pool_id}/clone')
        return structure(response, operations.PoolCloneOperation)

    def create_pool(self, pool: Pool) -> Pool:
        """Creates a new pool

        You can send a maximum of 20 requests of this kind per minute and 100 requests per day.

        Args:
            pool: New Pool with setted parameters.

        Returns:
            Pool: Created pool. With read-only fields.

        Example:
            How to create a new pool in a project.

            >>> toloka_client = toloka.TolokaClient(your_token, 'PRODUCTION')
            >>> new_pool = toloka.pool.Pool(
            >>>     project_id=existing_project_id,
            >>>     private_name='Pool 1',
            >>>     may_contain_adult_content=False,
            >>>     will_expire=datetime.datetime.utcnow() + datetime.timedelta(days=365),
            >>>     reward_per_assignment=0.01,
            >>>     assignment_max_duration_seconds=60*20,
            >>>     defaults=toloka.pool.Pool.Defaults(default_overlap_for_new_task_suites=3),
            >>>     filter=toloka.filter.Languages.in_('EN'),
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
        logger.info(f'A new pool with ID "{result.id}" has been created. Link to open in web interface: {self.url}/requester/project/{result.project_id}/pool/{result.id}')
        return result

    @expand('request')
    def find_pools(self, request: search_requests.PoolSearchRequest,
                   sort: Union[List[str], search_requests.PoolSortItems, None] = None,
                   limit: Optional[int] = None) -> search_results.PoolSearchResult:
        """Finds all pools that match certain rules

        As a result, it returns an object that contains the first part of the found pools and whether there
        are any more results.
        It is better to use the "get_pools" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search pools.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 300.
                Defaults to None, in which case it returns first 20 results.

        Returns:
            search_results.PoolSearchResult: The first "limit" pools in "items".
                And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.PoolSortItems)
        response = self._search_request('get', '/v1/pools', request, sort, limit)
        return structure(response, search_results.PoolSearchResult)

    def get_pool(self, pool_id: str) -> Pool:
        """Reads one specific pool

        Args:
            pool_id: ID of the pool.

        Returns:
            Pool: The pool.
        """
        response = self._request('get', f'/v1/pools/{pool_id}')
        return structure(response, Pool)

    @expand('request')
    def get_pools(self, request: search_requests.PoolSearchRequest) -> Generator[Pool, None, None]:
        """Finds all pools that match certain rules and returns them in an iterable object

        Unlike find_pools, returns generator. Does not sort pools.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search pools.

        Yields:
            Pool: The next object corresponding to the request parameters.

        Example:
            How to get all open pools from project.

            >>> open_pools = toloka_client.get_pools(project_id=my_project_id, status='OPEN')
            ...

            How to get all pools from project.

            >>> all_pools = toloka_client.get_pools(project_id=my_project_id)
            ...
        """
        return self._find_all(self.find_pools, request)

    def open_pool(self, pool_id: str) -> Pool:
        """Starts distributing tasks from the pool

        Performers will see your tasks only after that call.

        Args:
            pool_id: ID of the pool that will be started.

        Returns:
            Pool: Pool object with new status.
        """
        operation = self.open_pool_async(pool_id)
        operation = self.wait_operation(operation)
        return self.get_pool(operation.parameters.pool_id)

    def open_pool_async(self, pool_id: str) -> operations.PoolOpenOperation:
        """Starts distributing tasks from the pool, asynchronous version

        Performers will see your tasks only after that call.

        Args:
            pool_id: ID of the pool that will be started.

        Returns:
            PoolOpenOperation: An operation upon completion of which you can get the pool with new status.
        """
        response = self._request('post', f'/v1/pools/{pool_id}/open')
        return structure(response, operations.PoolOpenOperation)

    @expand('request')
    def patch_pool(self, pool_id: str, request: PoolPatchRequest) -> Pool:
        """Changes the priority of the pool issue

        Args:
            pool_id: ID of the pool that will be patched.
            request: New priority of the pool.

        Returns:
            Pool: Object with updated priority.

        Example:
            How to set highest priority to some pool.

            >>> toloka_client = toloka.TolokaClient(your_token, 'PRODUCTION')
            >>> patched_pool = toloka_client.patch_pool(existing_pool_id, 100)
            >>> print(patched_pool.priority)
            ...
        """
        response = self._request('patch', f'/v1/pools/{pool_id}', json=unstructure(request))
        return structure(response, Pool)

    def update_pool(self, pool_id: str, pool: Pool) -> Pool:
        """Makes changes to the pool

        Args:
            pool_id: ID of the pool that will be changed.
            pool: A pool object with all the fields: those that will be updated and those that will not.

        Returns:
            Pool: Pool object with all fields.
        """
        if pool.type == Pool.Type.TRAINING:
            raise ValueError('Training pools are not supported')
        response = self._request('put', f'/v1/pools/{pool_id}', json=unstructure(pool))
        return structure(response, Pool)

    # Training section

    def archive_training(self, training_id: str) -> Training:
        """Sends training to archive

        The training must be in the status "closed".
        The archived training is not deleted. You can access it when you will need it.

        Args:
            training_id: ID of training that will be archived.

        Returns:
            Training: Object with updated status.
        """
        operation = self.archive_training_async(training_id)
        operation = self.wait_operation(operation)
        return self.get_training(operation.parameters.training_id)

    def archive_training_async(self, training_id: str) -> operations.TrainingArchiveOperation:
        """Sends training to archive, asynchronous version

        The training must be in the status "closed".
        The archived training is not deleted. You can access it when you will need it.

        Args:
            training_id: ID of training that will be archived.

        Returns:
            TrainingArchiveOperation: An operation upon completion of which you can get the training with updated status.
        """
        response = self._request('post', f'/v1/trainings/{training_id}/archive')
        return structure(response, operations.TrainingArchiveOperation)

    def close_training(self, training_id: str) -> Training:
        """Stops distributing tasks from the training

        Args:
            training_id: ID of the training that will be closed.

        Returns:
            Training: Training object with new status.
        """
        operation = self.close_training_async(training_id)
        operation = self.wait_operation(operation)
        return self.get_training(operation.parameters.training_id)

    def close_training_async(self, training_id: str) -> operations.TrainingCloseOperation:
        """Stops distributing tasks from the training, asynchronous version

        Args:
            training_id: ID of the training that will be closed.

        Returns:
            TrainingCloseOperation: An operation upon completion of which you can get the training with updated status.
        """
        response = self._request('post', f'/v1/trainings/{training_id}/close')
        return structure(response, operations.TrainingCloseOperation)

    def clone_training(self, training_id: str) -> Training:
        """Duplicates existing training

        An empty training with the same parameters will be created.
        A new training will be attached to the same project.

        Args:
            training_id: ID of the existing training.

        Returns:
            Training: New training.
        """
        operation = self.clone_training_async(training_id)
        operation = self.wait_operation(operation)
        result = self.get_training(operation.details.training_id)
        logger.info(f'A new training with ID "{result.id}" has been cloned. Link to open in web interface: {self.url}/requester/project/{result.project_id}/training/{result.id}')
        return result

    def clone_training_async(self, training_id: str) -> operations.TrainingCloneOperation:
        """Duplicates existing training, asynchronous version

        An empty training with the same parameters will be created.
        A new training will be attached to the same project.

        Args:
            training_id: ID of the existing training.

        Returns:
            TrainingCloneOperation: An operation upon completion of which you can get the new training.
        """
        response = self._request('post', f'/v1/trainings/{training_id}/clone')
        return structure(response, operations.TrainingCloneOperation)

    def create_training(self, training: Training) -> Training:
        """Creates a new training

        Args:
            training: New Training with setted parameters.

        Returns:
            Training: Created training. With read-only fields.

        Example:
            How to create a new training in a project.

            >>> new_training = toloka.training.Training(
            >>>     project_id=existing_project_id,
            >>>     private_name='Some training in my project',
            >>>     may_contain_adult_content=True,
            >>>     assignment_max_duration_seconds=10000,
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
        logger.info(f'A new training with ID "{result.id}" has been created. Link to open in web interface: {self.url}/requester/project/{result.project_id}/training/{result.id}')
        return result

    @expand('request')
    def find_trainings(self, request: search_requests.TrainingSearchRequest,
                       sort: Union[List[str], search_requests.TrainingSortItems, None] = None,
                       limit: Optional[int] = None) -> search_results.TrainingSearchResult:
        """Finds all trainings that match certain rules

        As a result, it returns an object that contains the first part of the found trainings and whether there
        are any more results.
        It is better to use the "get_trainings" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search trainings.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            search_results.PoolSearchResult: The first "limit" trainings in "items".
                And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.TrainingSortItems)
        response = self._search_request('get', '/v1/trainings', request, sort, limit)
        return structure(response, search_results.TrainingSearchResult)

    def get_training(self, training_id: str) -> Training:
        """Reads one specific training

        Args:
            training_id: ID of the training.

        Returns:
            Training: The training.
        """
        response = self._request('get', f'/v1/trainings/{training_id}')
        return structure(response, Training)

    @expand('request')
    def get_trainings(self, request: search_requests.TrainingSearchRequest) -> Generator[Training, None, None]:
        """Finds all trainings that match certain rules and returns them in an iterable object

        Unlike find_trainings, returns generator. Does not sort trainings.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search trainings.

        Yields:
            Training: The next object corresponding to the request parameters.

        Example:
            How to get all trainings in project.

            >>> trainings = toloka_client.get_trainings(project_id=project_id)
            ...
        """
        return self._find_all(self.find_trainings, request)

    def open_training(self, training_id: str) -> Training:
        """Starts distributing tasks from the training

        Args:
            training_id: ID of the training that will be started.

        Returns:
            Training: Training object with new status.
        """
        operation = self.open_training_async(training_id)
        operation = self.wait_operation(operation)
        return self.get_training(operation.parameters.training_id)

    def open_training_async(self, training_id: str) -> operations.TrainingOpenOperation:
        """Starts distributing tasks from the training, asynchronous version

        Args:
            training_id: ID of the training that will be started.

        Returns:
            TrainingOpenOperation: An operation upon completion of which you can get the training with new status.
        """
        response = self._request('post', f'/v1/trainings/{training_id}/open')
        return structure(response, operations.TrainingOpenOperation)

    def update_training(self, training_id: str, training: Training) -> Training:
        """Makes changes to the training

        Args:
            training_id: ID of the training that will be changed.
            training: A training object with all the fields: those that will be updated and those that will not.

        Returns:
            Training: Training object with all fields.
        """
        response = self._request('put', f'/v1/trainings/{training_id}', json=unstructure(training))
        return structure(response, Training)

    # Skills section

    @expand('skill')
    def create_skill(self, skill: Skill) -> Skill:
        """Creates a new Skill

        You can send a maximum of 10 requests of this kind per minute and 100 requests per day.

        Args:
            skill: New Skill with setted parameters.

        Returns:
            Skill: Created skill. With read-only fields.

        Example:
            How to create new skill.

            >>> new_skill = toloka_client.create_skill(
            >>>     name='Area selection of road signs',
            >>>     public_requester_description={
            >>>         'EN': 'Performer is annotating road signs',
            >>>         'RU': 'Как исполнитель размечает дорожные знаки',
            >>>     },
            >>> )
            >>> print(new_skill.id)
            ...
        """
        response = self._request('post', '/v1/skills', json=unstructure(skill))
        result = structure(response, Skill)
        logger.info(f'A new skill with ID "{result.id}" has been created. Link to open in web interface: {self.url}/requester/quality/skill/{result.id}')
        return result

    @expand('request')
    def find_skills(self, request: search_requests.SkillSearchRequest,
                    sort: Union[List[str], search_requests.SkillSortItems, None] = None,
                    limit: Optional[int] = None) -> search_results.SkillSearchResult:
        """Finds all skills that match certain rules

        As a result, it returns an object that contains the first part of the found skills and whether there
        are any more results.
        It is better to use the "get_skills" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search skills.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            SkillSearchResult: The first "limit" skills in "items".
                And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.SkillSortItems)
        response = self._search_request('get', '/v1/skills', request, sort, limit)
        return structure(response, search_results.SkillSearchResult)

    def get_skill(self, skill_id: str) -> Skill:
        """Reads one specific skill

        Args:
            skill_id: ID of the skill.

        Returns:
            Skill: The skill.
        """
        response = self._request('get', f'/v1/skills/{skill_id}')
        return structure(response, Skill)

    @expand('request')
    def get_skills(self, request: search_requests.SkillSearchRequest) -> Generator[Skill, None, None]:
        """Finds all skills that match certain rules and returns them in an iterable object

        Unlike find_skills, returns generator. Does not sort skills.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search skills.

        Yields:
            Skill: The next object corresponding to the request parameters.

        Example:
            How to check that a skill exists.

            >>> segmentation_skill = next(toloka_client.get_skills(name='Area selection of road signs'), None)
            >>> if segmentation_skill:
            >>>     print(f'Segmentation skill already exists, with id {segmentation_skill.id}')
            >>> else:
            >>>     print('Create new segmentation skill here')
            ...
        """
        return self._find_all(self.find_skills, request)

    def update_skill(self, skill_id: str, skill: Skill) -> Skill:
        """Makes changes to the skill

        Args:
            skill_id: ID of the training that will be changed.
            skill: A skill object with all the fields: those that will be updated and those that will not.

        Returns:
            Skill: Modified skill object with all fields.
        """
        response = self._request('put', f'/v1/skills/{skill_id}', json=unstructure(skill))
        return structure(response, Skill)

    # Statistics section

    def get_analytics(self, stats: List[AnalyticsRequest]) -> operations.Operation:
        """Sends analytics queries, for example, to estimate the percentage of completed tasks in the pool

        Only pool analytics queries are available.
        The values of different analytical metrics will be returned in the "details" field of the operation when it is
        completed. See the example.
        You can request up to 10 metrics at a time.

        Args:
            stats: Analytics queries list.

        Returns:
            operations.Operation: An operation that you can wait for to get the required statistics.

        Example:
            How to get task completion percentage for one pool.

            >>> from toloka.client.analytics_request import CompletionPercentagePoolAnalytics
            >>> operation = toloka_client.get_analytics([CompletionPercentagePoolAnalytics(subject_id=pool_id)])
            >>> operation = toloka_client.wait_operation(operation)
            >>> print(op.details['value'][0]['result']['value'])
            92
        """
        response = self._request('post', '/staging/analytics-2', json=unstructure(stats))
        return structure(response, operations.Operation)

    # Task section

    @expand('parameters')
    def create_task(self, task: Task, parameters: Optional[task.CreateTaskParameters] = None) -> Task:
        """Creates a new task

        It's better to use "create_tasks", if you need to insert several tasks.
        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

        Args:
            task: Task that need to be created.
            parameters: Parameters for Task creation controlling. Defaults to None.
                Allows you to use default overlap and start pool after task creation.

        Returns:
            Task: Created task.
        """
        response = self._request('post', '/v1/tasks', json=unstructure(task), params=unstructure(parameters))
        return structure(response, Task)

    @expand('parameters')
    def create_tasks(self, tasks: List[Task], parameters: Optional[task.CreateTasksParameters] = None) -> batch_create_results.TaskBatchCreateResult:
        """Creates many tasks in pools

        By default uses asynchronous operation inside. It's better not to set "async_mode=False", if you not understand
        clearly why you need it.
        Tasks can be from different pools. You can insert both regular tasks and golden-tasks.
        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        Recomended maximum of 10,000 task per request if async_mode is True.

        Args:
            tasks: List of tasks, that will be created.
            parameters: Parameters for Tasks creation controlling. Defaults to None, in which case the asynchronous
                operations is used.

        Returns:
            batch_create_results.TaskBatchCreateResult: Result of tasks creating. Contains created tasks in "items" and
                problems in "validation_errors".

        Raises:
            ValidationApiError: If no tasks were created, or skip_invalid_items==False and there is a problem when
                checking any task.

        Example:
            How to create regular tasks from csv.

            >>> dataset = pandas.read_csv('dataset.tsv', sep='\t')
            >>> tasks = [
            >>>     toloka.task.Task(input_values={'image': url}, pool_id=existing_pool_id)
            >>>     for url in dataset['image'].values[:50]
            >>> ]
            >>> created_result = toloka_client.create_tasks(tasks, allow_defaults=True)
            >>> print(len(created_result.items))
            50

            How to create golden-tasks.

            >>> dataset = pd.read_csv('dateset.tsv', sep=';')
            >>> golden_tasks = []
            >>> for _, row in dataset.iterrows():
            >>>     golden_tasks.append(
            >>>             toloka.task.Task(
            >>>                 input_values={'image': row['image']},
            >>>                 known_solutions = [toloka.task.BaseTask.KnownSolution(output_values={'animal': row['label']})],
            >>>                 pool_id = existing_pool_id,
            >>>             )
            >>>         )
            >>> created_result = toloka_client.create_tasks(golden_tasks, allow_defaults=True)
            >>> print(len(created_result.items))
            10
        """
        if not parameters:
            parameters = task.CreateTasksParameters()
        return self._sync_via_async(
            objects=tasks,
            parameters=parameters,
            url='/v1/tasks',
            result_type=batch_create_results.TaskBatchCreateResult,
            operation_type=operations.TasksCreateOperation,
            output_id_field='task_id',
            get_method=self.get_tasks
        )

    @expand('parameters')
    def create_tasks_async(self, tasks: List[Task], parameters: Optional[task.CreateTasksParameters] = None) -> operations.TasksCreateOperation:
        """Creates many tasks in pools, asynchronous version

        You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
        Recomended maximum of 10,000 task per request if async_mode is True.

        Args:
            tasks: List of tasks, that will be created.
            parameters: Parameters for Tasks creation controlling. Defaults to None.

        Returns:
            TasksCreateOperation: An operation upon completion of which you can get the created tasks.
        """
        params = {**(unstructure(parameters) or {}), 'async_mode': True}
        response = self._request('post', '/v1/tasks', json=unstructure(tasks), params=params)
        return structure(response, operations.TasksCreateOperation)

    @expand('request')
    def find_tasks(self, request: search_requests.TaskSearchRequest,
                   sort: Union[List[str], search_requests.TaskSortItems, None] = None,
                   limit: Optional[int] = None) -> search_results.TaskSearchResult:
        """Finds all tasks that match certain rules

        As a result, it returns an object that contains the first part of the found tasks and whether there
        are any more results.
        It is better to use the "get_tasks" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search tasks.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100 000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            TaskSearchResult: The first "limit" tasks in "items". And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.TaskSortItems)
        response = self._search_request('get', '/v1/tasks', request, sort, limit)
        return structure(response, search_results.TaskSearchResult)

    def get_task(self, task_id: str) -> Task:
        """Reads one specific task

        Args:
            task_id: ID of the task.

        Returns:
            Task: The task.
        """
        response = self._request('get', f'/v1/tasks/{task_id}')
        return structure(response, Task)

    @expand('request')
    def get_tasks(self, request: search_requests.TaskSearchRequest) -> Generator[Task, None, None]:
        """Finds all tasks that match certain rules and returns them in an iterable object

        Unlike find_tasks, returns generator. Does not sort tasks.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search tasks.

        Yields:
            Task: The next object corresponding to the request parameters.
        """
        return self._find_all(self.find_tasks, request)

    @expand('patch')
    def patch_task(self, task_id: str, patch: task.TaskPatch) -> Task:
        """Changes the task overlap

        Args:
            task_id: ID of the task that will be changed.
            patch: New overlap value.

        Returns:
            Task: Task with updated fields.
        """
        response = self._request('patch', f'/v1/tasks/{task_id}', json=unstructure(patch))
        return structure(response, Task)

    @expand('patch')
    def patch_task_overlap_or_min(self, task_id: str, patch: task.TaskOverlapPatch) -> Task:
        """Stops issuing the task

        Args:
            task_id: ID of the task.
            patch: New overlap value.

        Returns:
            Task: Task with updated fields.
        """
        response = self._request('patch', f'/v1/tasks/{task_id}/set-overlap-or-min', json=unstructure(patch))
        return structure(response, Task)

    # Task suites section

    @expand('parameters')
    def create_task_suite(self, task_suite: TaskSuite, parameters: Optional[task_suite.TaskSuiteCreateRequestParameters] = None) -> TaskSuite:
        """Creates a new task suite

        Generally, you don't need to create a task set yourself, because you can create tasks and Toloka will create
        task suites for you. Use this method only then you need to group specific tasks in one suite or to set a
        different parameters on different tasks suites.
        It's better to use "create_task_suites", if you need to insert several task suites.
        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.

        Args:
            task_suite: Task suite that need to be created.
            parameters: Parameters for TaskSuite creation controlling. Defaults to None.

        Returns:
            TaskSuite: Created task suite.
        """
        params = {**(unstructure(parameters) or {}), 'async_mode': False}
        response = self._request('post', '/v1/task-suites', json=unstructure(task_suite), params=unstructure(params))
        return structure(response, TaskSuite)

    @expand('parameters')
    def create_task_suites(self, task_suites: List[TaskSuite], parameters: Optional[task_suite.TaskSuiteCreateRequestParameters] = None) -> batch_create_results.TaskSuiteBatchCreateResult:
        """Creates many task suites in pools

        Generally, you don't need to create a task set yourself, because you can create tasks and Toloka will create
        task suites for you. Use this method only then you need to group specific tasks in one suite or to set a
        different parameters on different tasks suites.
        By default uses asynchronous operation inside. It's better not to set "async_mode=False", if you not understand
        clearly why you need it.
        Task suites can be from different pools. You can insert both regular tasks and golden-tasks.
        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Recomended maximum of 10,000 task suites per request if async_mode is True.

        Args:
            task_suites: List of task suites, that will be created.
            parameters: Parameters for TaskSuite creation controlling. Defaults to None, in which case the asynchronous
                operations is used.

        Returns:
            TaskSuiteBatchCreateResult: Result of task suites creating. Contains created task suites in "items" and
                problems in "validation_errors".

        Raises:
            ValidationApiError: If no tasks were created, or skip_invalid_items==False and there is a problem when
                checking any task.
        """
        if not parameters:
            parameters = task_suite.TaskSuiteCreateRequestParameters()
        return self._sync_via_async(
            objects=task_suites,
            parameters=parameters,
            url='/v1/task-suites',
            result_type=batch_create_results.TaskBatchCreateResult,
            operation_type=operations.TaskSuiteCreateBatchOperation,
            output_id_field='task_suite_id',
            get_method=self.get_task_suites
        )

    @expand('parameters')
    def create_task_suites_async(self, task_suites: List[TaskSuite], parameters: Optional[task_suite.TaskSuiteCreateRequestParameters] = None) -> operations.TaskSuiteCreateBatchOperation:
        """Creates many task suites in pools, asynchronous version

        You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.
        Recomended maximum of 10,000 task suites per request.

        Args:
            task_suites: List of task suites, that will be created.
            parameters: Parameters for TaskSuite creation controlling.

        Returns:
            TaskSuiteCreateBatchOperation: An operation upon completion of which you can get the created teask suites.
        """
        params = {**(unstructure(parameters) or {}), 'async_mode': True}
        response = self._request('post', '/v1/task-suites', json=unstructure(task_suites), params=params)
        return structure(response, operations.TaskSuiteCreateBatchOperation)

    @expand('request')
    def find_task_suites(self, request: search_requests.TaskSuiteSearchRequest,
                         sort: Union[List[str], search_requests.TaskSuiteSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.TaskSuiteSearchResult:
        """Finds all task suites that match certain rules

        As a result, it returns an object that contains the first part of the found task suites and whether there
        are any more results.
        It is better to use the "get_task_suites" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search task suites.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned. The maximum is 100 000.
                Defaults to None, in which case it returns first 50 results.

        Returns:
            TaskSuiteSearchResult: The first "limit" task suites in "items". And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.TaskSuiteSortItems)
        response = self._search_request('get', '/v1/task-suites', request, sort, limit)
        return structure(response, search_results.TaskSuiteSearchResult)

    def get_task_suite(self, task_suite_id: str) -> TaskSuite:
        """Reads one specific task suite

        Args:
            task_suite_id: ID of the task suite.

        Returns:
            TaskSuite: The task suite.
        """
        response = self._request('get', f'/v1/task-suites/{task_suite_id}')
        return structure(response, TaskSuite)

    @expand('request')
    def get_task_suites(self, request: search_requests.TaskSuiteSearchRequest) -> Generator[TaskSuite, None, None]:
        """Finds all task suites that match certain rules and returns them in an iterable object

        Unlike find_task_suites, returns generator. Does not sort task suites.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search task suites.

        Yields:
            TaskSuite: The next object corresponding to the request parameters.
        """
        return self._find_all(self.find_task_suites, request)

    @expand('patch')
    def patch_task_suite(self, task_suite_id: str, patch: task_suite.TaskSuitePatch) -> TaskSuite:
        """Changes the task suite overlap or priority

        Args:
            task_suite_id: ID of the task suite that will be changed.
            patch: New values.

        Returns:
            TaskSuite: Task suite with updated fields.
        """
        body = unstructure(patch)
        params = {'open_pool': body.pop('open_pool')} if 'open_pool' in body else None
        response = self._request('patch', f'/v1/task-suites/{task_suite_id}', json=body, params=params)
        return structure(response, TaskSuite)

    @expand('patch')
    def patch_task_suite_overlap_or_min(self, task_suite_id: str, patch: task_suite.TaskSuiteOverlapPatch) -> TaskSuite:
        """Stops issuing the task suites

        Args:
            task_suite_id: ID of the task suite.
            patch: New overlap value.

        Returns:
            TaskSuite: Task suite with updated fields.
        """
        body = unstructure(patch)
        params = {'open_pool': body.pop('open_pool')} if 'open_pool' in body else None
        response = self._request('patch', f'/v1/task-suites/{task_suite_id}/set-overlap-or-min', json=body, params=params)
        return structure(response, TaskSuite)

    # Operations section

    def get_operation(self, operation_id: str) -> operations.Operation:
        """Reads information about operation

        All asynchronous actions in Toloka works via operations. If you have some "Operation" usually you need to use
        "wait_operation" method.

        Args:
            operation_id: ID of the operation.

        Returns:
            Operation: The operation.
        """
        response = self._request('get', f'/v1/operations/{operation_id}')
        return structure(response, operations.Operation)

    def wait_operation(self, op: operations.Operation, timeout: datetime.timedelta = datetime.timedelta(minutes=10)) -> operations.Operation:
        """Waits for the operation to complete, and return it

        Args:
            op: ID of the operation.
            timeout: How long to wait. Defaults to 10 minutes.

        Raises:
            TimeoutError: Raises it if the timeout has expired and the operation is still not completed.

        Returns:
            Operation: Completed operation.
        """
        default_time_to_wait = datetime.timedelta(seconds=1)
        default_initial_delay = datetime.timedelta(milliseconds=500)

        if op.is_completed():
            return op

        utcnow = datetime.datetime.utcnow()
        wait_until_time = utcnow + timeout

        if not op.started or utcnow - op.started < default_initial_delay:
            time.sleep(default_initial_delay.total_seconds())

        while True:
            op = self.get_operation(op.id)
            if op.is_completed():
                return op
            time.sleep(default_time_to_wait.total_seconds())
            if datetime.datetime.utcnow() > wait_until_time:
                raise TimeoutError

    def get_operation_log(self, operation_id: str) -> List[OperationLogItem]:
        """Reads information about validation errors and which task (or task suites) were created

        You don't need to call this method if you use "create_tasks" for creating tasks ("create_task_suites" for task suites).
        By asynchronous creating multiple tasks (or task sets) you can get the operation log.
        Logs are only available for the last month.

        Args:
            operation_id: ID of the operation.

        Returns:
            List[OperationLogItem]: Logs for the operation.
        """
        response = self._request('get', f'/v1/operations/{operation_id}/log')
        return structure(response, List[OperationLogItem])

    # User bonus

    def create_user_bonus(self, user_bonus: UserBonus, parameters: Optional[UserBonusCreateRequestParameters] = None) -> UserBonus:
        """Issues payments directly to the performer

        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonus: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonus: Created bonus.

        Example:
            How to create bonus with message for specific assignment.

            >>> new_bonus = toloka_client.create_user_bonus(
            >>>     UserBonus(
            >>>         user_id='1',
            >>>         amount='0.50',
            >>>         public_title='Perfect job!',
            >>>         public_message='You are the best performer EVER!'
            >>>         assignment_id='012345'
            >>>     )
            >>> )
        """
        response = self._request(
            'post', '/v1/user-bonuses', json=unstructure(user_bonus),
            params=({} if parameters is None else unstructure(parameters)),
        )
        return structure(response, UserBonus)

    @expand('parameters')
    def create_user_bonuses(self, user_bonuses: List[UserBonus], parameters: Optional[UserBonusCreateRequestParameters] = None) -> batch_create_results.UserBonusBatchCreateResult:
        """Creates many user bonuses

        Right now it's safer to use asynchronous version: "create_user_bonuses_async"
        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonuses: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonusBatchCreateResult: Result of user bonuses creating. Contains created user bonuses in "items" and
                problems in "validation_errors".
        """
        response = self._request(
            'post', '/v1/user-bonuses', json=unstructure(user_bonuses),
            params=({} if parameters is None else unstructure(parameters)),
        )
        return structure(response, batch_create_results.UserBonusBatchCreateResult)

    @expand('parameters')
    def create_user_bonuses_async(self, user_bonuses: List[UserBonus], parameters: Optional[UserBonusCreateRequestParameters] = None) -> operations.UserBonusCreateBatchOperation:
        """Issues payments directly to the performers, asynchronously creates many user bonuses

        You can send a maximum of 10,000 requests of this kind per day.

        Args:
            user_bonuses: To whom, how much to pay and for what.
            parameters: Parameters for UserBonus creation controlling.

        Returns:
            UserBonusCreateBatchOperation: An operation upon completion of which the bonuses can be considered created.
        """
        params = {'async_mode': True, **(unstructure(parameters) or {})}
        response = self._request('post', '/v1/user-bonuses', json=unstructure(user_bonuses), params=params)
        return structure(response, operations.UserBonusCreateBatchOperation)

    @expand('request')
    def find_user_bonuses(self, request: search_requests.UserBonusSearchRequest,
                          sort: Union[List[str], search_requests.UserBonusSortItems, None] = None,
                          limit: Optional[int] = None) -> search_results.UserBonusSearchResult:
        """Finds all user bonuses that match certain rules

        As a result, it returns an object that contains the first part of the found user bonuses and whether there
        are any more results.
        It is better to use the "get_user_bonuses" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user bonuses.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserBonusSearchResult: The first "limit" user bonuses in "items".
                And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.UserBonusSortItems)
        response = self._search_request('get', '/v1/user-bonuses', request, sort, limit)
        return structure(response, search_results.UserBonusSearchResult)

    def get_user_bonus(self, user_bonus_id: str) -> UserBonus:
        """Reads one specific user bonus

        Args:
            user_bonus_id: ID of the user bonus.

        Returns:
            UserBonus: The user bonus.
        """
        response = self._request('get', f'/v1/user-bonuses/{user_bonus_id}')
        return structure(response, UserBonus)

    @expand('request')
    def get_user_bonuses(self, request: search_requests.UserBonusSearchRequest) -> Generator[UserBonus, None, None]:
        """Finds all user bonuses that match certain rules and returns them in an iterable object

        Unlike find_user_bonuses, returns generator. Does not sort user bonuses.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user bonus.

        Yields:
            UserBonus: The next object corresponding to the request parameters.
        """
        return self._find_all(self.find_user_bonuses, request)

    # User restrictions

    @expand('request')
    def find_user_restrictions(self, request: search_requests.UserRestrictionSearchRequest,
                               sort: Union[List[str], search_requests.UserRestrictionSortItems, None] = None,
                               limit: Optional[int] = None) -> search_results.UserRestrictionSearchResult:
        """Finds all user restrictions that match certain rules

        As a result, it returns an object that contains the first part of the found user restrictions and whether there
        are any more results.
        It is better to use the "get_user_restriction" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user restrictions.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserRestrictionSearchResult: The first "limit" user restrictions in "items".
                And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.UserRestrictionSortItems)
        response = self._search_request('get', '/v1/user-restrictions', request, sort, limit)
        return structure(response, search_results.UserRestrictionSearchResult)

    def get_user_restriction(self, user_restriction_id: str) -> UserRestriction:
        """Reads one specific user restriction

        Args:
            user_restriction_id: ID of the user restriction.

        Returns:
            UserRestriction: The user restriction.
        """
        response = self._request('get', f'/v1/user-restrictions/{user_restriction_id}')
        return structure(response, UserRestriction)

    @expand('request')
    def get_user_restrictions(self, request: search_requests.UserRestrictionSearchRequest) -> Generator[UserRestriction, None, None]:
        """Finds all user restrictions that match certain rules and returns them in an iterable object

        Unlike find_user_restrictions, returns generator. Does not sort user restrictions.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user restrictions.

        Yields:
            UserRestriction: The next object corresponding to the request parameters.
        """
        return self._find_all(self.find_user_restrictions, request)

    def set_user_restriction(self, user_restriction: UserRestriction) -> UserRestriction:
        """Closes the performer's access to one or more projects

        Args:
            user_restriction: To whom and what to prohibit.

        Returns:
            UserRestriction: Created restriction object.
        """
        response = self._request('put', '/v1/user-restrictions', json=unstructure(user_restriction))
        return structure(response, UserRestriction)

    def delete_user_restriction(self, user_restriction_id: str) -> None:
        """Unlocks existing restriction

        Args:
            user_restriction_id: Restriction that should be removed.
        """
        self._raw_request('delete', f'/v1/user-restrictions/{user_restriction_id}')

    # Requester

    def get_requester(self) -> Requester:
        """Reads information about the customer and the account balance

        Returns:
            Requester: Object that contains all information about customer.
        """
        response = self._request('get', '/v1/requester')
        return structure(response, Requester)

    # User skills

    @expand('request')
    def find_user_skills(self, request: search_requests.UserSkillSearchRequest,
                         sort: Union[List[str], search_requests.UserSkillSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.UserSkillSearchResult:
        """Finds all user skills that match certain rules

        UserSkill describe the skill value for a specific performer.
        As a result, it returns an object that contains the first part of the found user skills and whether there
        are any more results.
        It is better to use the "get_user_skills" method, they allow to iterate trought all results
        and not just the first output.

        Args:
            request: How to search user skills.
            sort: How to sort result. Defaults to None.
            limit: Limit on the number of results returned.

        Returns:
            UserSkillSearchResult: The first "limit" user skills in "items".
                And a mark that there is more.
        """
        sort = None if sort is None else structure(sort, search_requests.UserSkillSortItems)
        response = self._search_request('get', '/v1/user-skills', request, sort, limit)
        return structure(response, search_results.UserSkillSearchResult)

    def get_user_skill(self, user_skill_id: str) -> UserSkill:
        """Gets the value of the user's skill

        UserSkill describe the skill value for a specific performer.

        Args:
            user_skill_id: ID of the user skill.

        Returns:
            UserSkill: The skill value.
        """
        response = self._request('get', f'/v1/user-skills/{user_skill_id}')
        return structure(response, UserSkill)

    @expand('request')
    def get_user_skills(self, request: search_requests.UserSkillSearchRequest) -> Generator[UserSkill, None, None]:
        """Finds all user skills that match certain rules and returns them in an iterable object

        UserSkill describe the skill value for a specific performer.
        Unlike find_user_skills, returns generator. Does not sort user skills.
        While iterating over the result, several requests to the Toloka server is possible.

        Args:
            request: How to search user skills.

        Yields:
            UserSkill: The next object corresponding to the request parameters.
        """
        return self._find_all(self.find_user_skills, request)

    @expand('request')
    def set_user_skill(self, request: SetUserSkillRequest) -> UserSkill:
        """Sets the skill value to the performer

        Args:
            request: To whom and what value of the skill to set.

        Returns:
            UserSkill: Сreated fact of skill installation.
        """
        response = self._request('put', '/v1/user-skills', json=unstructure(request))
        return structure(response, UserSkill)

    def delete_user_skill(self, user_skill_id: str) -> None:
        """Drop specific UserSkill

        UserSkill describe the skill value for a specific performer.

        Args:
            user_skill_id: ID of the fact that the performer has a skill to delete.
        """
        self._raw_request('delete', f'/v1/user-skills/{user_skill_id}')

    # Experimental section

    @expand('parameters')
    def get_assignments_df(self, pool_id: str, parameters: GetAssignmentsTsvParameters) -> pd.DataFrame:
        """Downloads assignments as pandas.DataFrame

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
        """
        logger.warning('Experimental method')
        response = self._raw_request('get', f'/new/requester/pools/{pool_id}/assignments.tsv',
                                     params=unstructure(parameters))
        return pd.read_csv(io.StringIO(response.text), delimiter='\t')
