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
from .exceptions import raise_on_api_error
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

    @unique
    class Environment(Enum):
        SANDBOX = 'https://sandbox.toloka.yandex.ru/api'
        PRODUCTION = 'https://toloka.yandex.ru/api'

    def __init__(
        self,
        token: str,
        environment: Union[Environment, str],
        retries: Union[int, Retry] = 3,
        timeout: Union[float, Tuple[float, float]] = 10.0
    ):
        if not isinstance(environment, TolokaClient.Environment):
            environment = TolokaClient.Environment[environment.upper()]
        self.token = token
        self.url = environment.value
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
        response = self.session.request(method, f'{self.url}{path}', **kwargs)
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

    # Aggregation section

    @expand('request')
    def aggregate_solutions_by_pool(self, request: aggregation.PoolAggregatedSolutionRequest) -> operations.AggregatedSolutionOperation:
        data = unstructure(request)
        response = self._request('post', '/v1/aggregated-solutions/aggregate-by-pool', json=data)
        return structure(response, operations.AggregatedSolutionOperation)

    @expand('request')
    def aggregate_solutions_by_task(self, request: aggregation.WeightedDynamicOverlapTaskAggregatedSolutionRequest) -> AggregatedSolution:
        response = self._request('post', '/v1/aggregated-solutions/aggregate-by-task', json=unstructure(request))
        return structure(response, AggregatedSolution)

    @expand('request')
    def find_aggregated_solutions(self, operation_id: str, request: search_requests.AggregatedSolutionSearchRequest,
                                  sort: Union[List[str], search_requests.AggregatedSolutionSortItems, None] = None,
                                  limit: Optional[int] = None) -> search_results.AggregatedSolutionSearchResult:
        sort = None if sort is None else structure(sort, search_requests.AggregatedSolutionSortItems)
        response = self._search_request('get', f'/v1/aggregated-solutions/{operation_id}', request, sort, limit)
        return structure(response, search_results.AggregatedSolutionSearchResult)

    # Assignments section

    def accept_assignment(self, assignment_id: str, public_comment: str) -> Assignment:
        return self.patch_assignment(assignment_id, public_comment=public_comment, status=Assignment.ACCEPTED)

    @expand('request')
    def find_assignments(self, request: search_requests.AssignmentSearchRequest,
                         sort: Union[List[str], search_requests.AssignmentSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.AssignmentSearchResult:
        sort = None if sort is None else structure(sort, search_requests.AssignmentSortItems)
        response = self._search_request('get', '/v1/assignments', request, sort, limit)
        return structure(response, search_results.AssignmentSearchResult)

    def get_assignment(self, assignment_id: str) -> Assignment:
        response = self._request('get', f'/v1/assignments/{assignment_id}')
        return structure(response, Assignment)

    @expand('request')
    def get_assignments(self, request: search_requests.AssignmentSearchRequest) -> Generator[Assignment, None, None]:
        return self._find_all(self.find_assignments, request)

    @expand('patch')
    def patch_assignment(self, assignment_id: str, patch: AssignmentPatch) -> Assignment:
        response = self._request('patch', f'/v1/assignments/{assignment_id}', json=unstructure(patch))
        return structure(response, Assignment)

    def reject_assignment(self, assignment_id: str, public_comment: str) -> Assignment:
        return self.patch_assignment(assignment_id, public_comment=public_comment, status=Assignment.REJECTED)

    # Attachment section

    @expand('request')
    def find_attachments(self, request: search_requests.AttachmentSearchRequest,
                         sort: Union[List[str], search_requests.AttachmentSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.AttachmentSearchResult:
        sort = None if sort is None else structure(sort, search_requests.AttachmentSortItems)
        response = self._search_request('get', '/v1/attachments', request, sort, limit)
        return structure(response, search_results.AttachmentSearchResult)

    def get_attachment(self, attachment_id: str) -> Attachment:
        response = self._request('get', f'/v1/attachments/{attachment_id}')
        return structure(response, Attachment)

    @expand('request')
    def get_attachments(self, request: search_requests.AttachmentSearchRequest) -> Generator[Attachment, None, None]:
        return self._find_all(self.find_attachments, request)

    def download_attachment(self, attachment_id: str, out: BinaryIO) -> None:
        response = self._raw_request('get', f'/v1/attachments/{attachment_id}/download', stream=True)
        for content in response.iter_content():
            out.write(content)

    # Message section

    def add_message_thread_to_folders(self, message_thread_id: str, folders: Union[List[Folder], MessageThreadFolders]) -> MessageThread:
        if not isinstance(folders, MessageThreadFolders):
            folders = structure({'folders': folders}, MessageThreadFolders)
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/add-to-folders', json=unstructure(folders))
        return structure(response, MessageThread)

    @expand('compose')
    def compose_message_thread(self, compose: MessageThreadCompose) -> MessageThread:
        response = self._request('post', '/v1/message-threads/compose', json=unstructure(compose))
        return structure(response, MessageThread)

    @expand('request')
    def find_message_threads(self, request: search_requests.MessageThreadSearchRequest,
                             sort: Union[List[str], search_requests.MessageThreadSortItems, None] = None,
                             limit: Optional[int] = None) -> search_results.MessageThreadSearchResult:
        sort = None if sort is None else structure(sort, search_requests.MessageThreadSortItems)
        response = self._search_request('get', '/v1/message-threads', request, sort, limit)
        return structure(response, search_results.MessageThreadSearchResult)

    def reply_message_thread(self, message_thread_id: str, reply: MessageThreadReply) -> MessageThread:
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/reply', json=unstructure(reply))
        return structure(response, MessageThread)

    @expand('request')
    def get_message_threads(self, request: search_requests.MessageThreadSearchRequest) -> Generator[MessageThread, None, None]:
        return self._find_all(self.find_message_threads, request)

    def remove_message_thread_from_folders(self, message_thread_id: str, folders: Union[List[Folder], MessageThreadFolders]) -> MessageThread:
        if not isinstance(folders, MessageThreadFolders):
            folders = structure({'folders': folders}, MessageThreadFolders)
        response = self._request('post', f'/v1/message-threads/{message_thread_id}/remove-from-folders', json=unstructure(folders))
        return structure(response, MessageThread)

    # Project section

    def archive_project(self, project_id: str) -> operations.ProjectArchiveOperation:
        response = self._request('post', f'/v1/projects/{project_id}/archive')
        return structure(response, operations.ProjectArchiveOperation)

    def create_project(self, project: Project) -> Project:
        response = self._request('post', '/v1/projects', json=unstructure(project))
        return structure(response, Project)

    @expand('request')
    def find_projects(self, request: search_requests.ProjectSearchRequest,
                      sort: Union[List[str], search_requests.ProjectSortItems, None] = None,
                      limit: Optional[int] = None) -> search_results.ProjectSearchResult:
        sort = None if sort is None else structure(sort, search_requests.ProjectSortItems)
        response = self._search_request('get', '/v1/projects', request, sort, limit)
        return structure(response, search_results.ProjectSearchResult)

    def get_project(self, project_id: str) -> Project:
        response = self._request('get', f'/v1/projects/{project_id}')
        return structure(response, Project)

    @expand('request')
    def get_projects(self, request: search_requests.ProjectSearchRequest) -> Generator[Project, None, None]:
        return self._find_all(self.find_projects, request)

    def update_project(self, project_id: str, project: Project) -> Project:
        response = self._request('put', f'/v1/projects/{project_id}', json=unstructure(project))
        return structure(response, Project)

    # Pool section

    def archive_pool(self, pool_id: str) -> operations.PoolArchiveOperation:
        response = self._request('post', f'/v1/pools/{pool_id}/archive')
        return structure(response, operations.PoolArchiveOperation)

    def close_pool(self, pool_id: str) -> operations.PoolCloseOperation:
        response = self._request('post', f'/v1/pools/{pool_id}/close')
        return structure(response, operations.PoolCloseOperation)

    def close_pool_for_update(self, pool_id: str) -> operations.PoolCloseOperation:
        response = self._request('post', f'/v1/pools/{pool_id}/close-for-update')
        return structure(response, operations.PoolCloseOperation)

    def clone_pool(self, pool_id: str) -> operations.PoolCloneOperation:
        response = self._request('post', f'/v1/pools/{pool_id}/clone')
        return structure(response, operations.PoolCloneOperation)

    def create_pool(self, pool: Pool) -> Pool:
        if pool.type == Pool.Type.TRAINING:
            raise ValueError('Training pools are not supported')

        response = self._request('post', '/v1/pools', json=unstructure(pool))
        return structure(response, Pool)

    @expand('request')
    def find_pools(self, request: search_requests.PoolSearchRequest,
                   sort: Union[List[str], search_requests.PoolSortItems, None] = None,
                   limit: Optional[int] = None) -> search_results.PoolSearchResult:
        sort = None if sort is None else structure(sort, search_requests.PoolSortItems)
        response = self._search_request('get', '/v1/pools', request, sort, limit)
        return structure(response, search_results.PoolSearchResult)

    def get_pool(self, pool_id: str) -> Pool:
        response = self._request('get', f'/v1/pools/{pool_id}')
        return structure(response, Pool)

    @expand('request')
    def get_pools(self, request: search_requests.PoolSearchRequest) -> Generator[Pool, None, None]:
        return self._find_all(self.find_pools, request)

    def open_pool(self, pool_id: str) -> operations.PoolOpenOperation:
        response = self._request('post', f'/v1/pools/{pool_id}/open')
        return structure(response, operations.PoolOpenOperation)

    @expand('request')
    def patch_pool(self, pool_id: str, request: PoolPatchRequest) -> Pool:
        response = self._request('patch', f'/v1/pools/{pool_id}', json=unstructure(request))
        return structure(response, Pool)

    def update_pool(self, pool_id: str, pool: Pool) -> Pool:
        if pool.type == Pool.Type.TRAINING:
            raise ValueError('Training pools are not supported')
        response = self._request('put', f'/v1/pools/{pool_id}', json=unstructure(pool))
        return structure(response, Pool)

    # Training section

    def archive_training(self, training_id: str) -> operations.TrainingArchiveOperation:
        response = self._request('post', f'/v1/trainings/{training_id}/archive')
        return structure(response, operations.TrainingArchiveOperation)

    def close_training(self, training_id: str) -> operations.TrainingCloseOperation:
        response = self._request('post', f'/v1/trainings/{training_id}/close')
        return structure(response, operations.TrainingCloseOperation)

    def clone_training(self, training_id: str) -> operations.TrainingCloneOperation:
        response = self._request('post', f'/v1/trainings/{training_id}/clone')
        return structure(response, operations.TrainingCloneOperation)

    def create_training(self, training: Training) -> Training:
        response = self._request('post', '/v1/trainings', json=unstructure(training))
        return structure(response, Training)

    @expand('request')
    def find_trainings(self, request: search_requests.TrainingSearchRequest,
                       sort: Union[List[str], search_requests.TrainingSortItems, None] = None,
                       limit: Optional[int] = None) -> search_results.TrainingSearchResult:
        sort = None if sort is None else structure(sort, search_requests.TrainingSortItems)
        response = self._search_request('get', '/v1/trainings', request, sort, limit)
        return structure(response, search_results.TrainingSearchResult)

    def get_training(self, training_id: str) -> Training:
        response = self._request('get', f'/v1/trainings/{training_id}')
        return structure(response, Training)

    @expand('request')
    def get_trainings(self, request: search_requests.TrainingSearchRequest) -> Generator[Training, None, None]:
        return self._find_all(self.find_trainings, request)

    def open_training(self, training_id: str) -> operations.TrainingOpenOperation:
        response = self._request('post', f'/v1/trainings/{training_id}/open')
        return structure(response, operations.TrainingOpenOperation)

    def update_training(self, training_id: str, training: Training) -> Training:
        response = self._request('put', f'/v1/trainings/{training_id}', json=unstructure(training))
        return structure(response, Training)

    # Skills section

    @expand('skill')
    def create_skill(self, skill: Skill) -> Skill:
        response = self._request('post', '/v1/skills', json=unstructure(skill))
        return structure(response, Skill)

    @expand('request')
    def find_skills(self, request: search_requests.SkillSearchRequest,
                    sort: Union[List[str], search_requests.SkillSortItems, None] = None,
                    limit: Optional[int] = None) -> search_results.SkillSearchResult:
        sort = None if sort is None else structure(sort, search_requests.SkillSortItems)
        response = self._search_request('get', '/v1/skills', request, sort, limit)
        return structure(response, search_results.SkillSearchResult)

    def get_skill(self, skill_id: str) -> Skill:
        response = self._request('get', f'/v1/skills/{skill_id}')
        return structure(response, Skill)

    @expand('request')
    def get_skills(self, request: search_requests.SkillSearchRequest) -> Generator[Skill, None, None]:
        return self._find_all(self.find_skills, request)

    def update_skill(self, skill_id: str, skill: Skill):
        response = self._request('put', f'/v1/skills/{skill_id}', json=unstructure(skill))
        return structure(response, Skill)

    # Statistics section

    def get_analytics(self, stats: List[AnalyticsRequest]) -> operations.Operation:
        response = self._request('post', '/staging/analytics-2', json=unstructure(stats))
        return structure(response, operations.Operation)

    # Task section

    @expand('parameters')
    def create_task(self, task: Task, parameters: Optional[task.CreateTaskParameters] = None) -> Task:
        response = self._request('post', '/v1/tasks', json=unstructure(task), params=unstructure(parameters))
        return structure(response, Task)

    @expand('parameters')
    def create_tasks(self, tasks: List[Task], parameters: Optional[task.CreateTasksParameters] = None) -> batch_create_results.TaskBatchCreateResult:
        response = self._request('post', '/v1/tasks', json=unstructure(tasks), params=unstructure(parameters))
        return structure(response, batch_create_results.TaskBatchCreateResult)

    @expand('parameters')
    def create_tasks_async(self, tasks: List[Task], parameters: Optional[task.CreateTasksAsyncParameters] = None) -> operations.TasksCreateOperation:
        params = {'async_mode': True, **(unstructure(parameters) or {})}
        response = self._request('post', '/v1/tasks', json=unstructure(tasks), params=params)
        return structure(response, operations.TasksCreateOperation)

    @expand('request')
    def find_tasks(self, request: search_requests.TaskSearchRequest,
                   sort: Union[List[str], search_requests.TaskSortItems, None] = None,
                   limit: Optional[int] = None) -> search_results.TaskSearchResult:
        sort = None if sort is None else structure(sort, search_requests.TaskSortItems)
        response = self._search_request('get', '/v1/tasks', request, sort, limit)
        return structure(response, search_results.TaskSearchResult)

    def get_task(self, task_id: str) -> Task:
        response = self._request('get', f'/v1/tasks/{task_id}')
        return structure(response, Task)

    @expand('request')
    def get_tasks(self, request: search_requests.TaskSearchRequest) -> Generator[Task, None, None]:
        return self._find_all(self.find_tasks, request)

    @expand('patch')
    def patch_task(self, task_id: str, patch: task.TaskPatch) -> Task:
        response = self._request('patch', f'/v1/tasks/{task_id}', json=unstructure(patch))
        return structure(response, Task)

    @expand('patch')
    def patch_task_overlap_or_min(self, task_id: str, patch: task.TaskOverlapPatch) -> Task:
        response = self._request('patch', f'/v1/tasks/{task_id}/set-overlap-or-min', json=unstructure(patch))
        return structure(response, Task)

    # Task suites section

    @expand('parameters')
    def create_task_suite(self, task_suite: TaskSuite, parameters: Optional[task_suite.TaskSuiteCreateRequestParameters] = None) -> TaskSuite:
        response = self._request('post', '/v1/task-suites', json=unstructure(task_suite), params=unstructure(parameters))
        return structure(response, TaskSuite)

    @expand('parameters')
    def create_task_suites(self, task_suites: List[TaskSuite], parameters: Optional[task_suite.TaskSuiteCreateRequestParameters] = None) -> batch_create_results.TaskSuiteBatchCreateResult:
        response = self._request('post', '/v1/task-suites', json=unstructure(task_suites), params=unstructure(parameters))
        return structure(response, batch_create_results.TaskSuiteBatchCreateResult)

    @expand('parameters')
    def create_task_suites_async(self, task_suites: List[TaskSuite], parameters: Optional[task_suite.TaskSuiteCreateRequestParameters] = None) -> operations.TaskSuiteCreateBatchOperation:
        params = {'async_mode': True, **(unstructure(parameters) or {})}
        response = self._request('post', '/v1/task-suites', json=unstructure(task_suites), params=params)
        return structure(response, operations.TaskSuiteCreateBatchOperation)

    @expand('request')
    def find_task_suites(self, request: search_requests.TaskSuiteSearchRequest,
                         sort: Union[List[str], search_requests.TaskSuiteSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.TaskSuiteSearchResult:
        sort = None if sort is None else structure(sort, search_requests.TaskSuiteSortItems)
        response = self._search_request('get', '/v1/task-suites', request, sort, limit)
        return structure(response, search_results.TaskSuiteSearchResult)

    def get_task_suite(self, task_suite_id: str) -> TaskSuite:
        response = self._request('get', f'/v1/task-suites/{task_suite_id}')
        return structure(response, TaskSuite)

    @expand('request')
    def get_task_suites(self, request: search_requests.TaskSuiteSearchRequest) -> Generator[TaskSuite, None, None]:
        return self._find_all(self.find_task_suites, request)

    @expand('patch')
    def patch_task_suite(self, task_suite_id: str, patch: task_suite.TaskSuitePatch) -> TaskSuite:
        body = unstructure(patch)
        params = {'open_pool': body.pop('open_pool')} if 'open_pool' in body else None
        response = self._request('patch', f'/v1/task-suites/{task_suite_id}', json=body, params=params)
        return structure(response, TaskSuite)

    @expand('patch')
    def patch_task_suite_overlap_or_min(self, task_suite_id: str, patch: task_suite.TaskSuiteOverlapPatch) -> TaskSuite:
        body = unstructure(patch)
        params = {'open_pool': body.pop('open_pool')} if 'open_pool' in body else None
        response = self._request('patch', f'/v1/task-suites/{task_suite_id}/set-overlap-or-min', json=body, params=params)
        return structure(response, TaskSuite)

    # Operations section

    def get_operation(self, operation_id: str) -> operations.Operation:
        response = self._request('get', f'/v1/operations/{operation_id}')
        return structure(response, operations.Operation)

    def wait_operation(self, op: operations.Operation) -> operations.Operation:

        default_time_to_wait = datetime.timedelta(seconds=1)
        default_timeout = datetime.timedelta(minutes=10)
        default_initial_delay = datetime.timedelta(milliseconds=500)

        if op.is_completed():
            return op

        utcnow = datetime.datetime.utcnow()
        timeout = utcnow + default_timeout

        if not op.started or utcnow - op.started < default_initial_delay:
            time.sleep(default_initial_delay.total_seconds())

        while True:
            op = self.get_operation(op.id)
            if op.is_completed():
                return op
            time.sleep(default_time_to_wait.total_seconds())
            if datetime.datetime.utcnow() > timeout:
                raise TimeoutError

    def get_operation_log(self, operation_id: str) -> List[OperationLogItem]:
        response = self._request('get', f'/v1/operations/{operation_id}/log')
        return structure(response, List[OperationLogItem])

    # User bonus

    def create_user_bonus(self, user_bonus: UserBonus, parameters: Optional[UserBonusCreateRequestParameters] = None) -> UserBonus:
        response = self._request(
            'post', '/v1/user-bonuses', json=unstructure(user_bonus),
            params=({} if parameters is None else unstructure(parameters)),
        )
        return structure(response, UserBonus)

    @expand('parameters')
    def create_user_bonuses(self, user_bonuses: List[UserBonus], parameters: Optional[UserBonusCreateRequestParameters] = None) -> batch_create_results.UserBonusBatchCreateResult:
        response = self._request(
            'post', '/v1/user-bonuses', json=unstructure(user_bonuses),
            params=({} if parameters is None else unstructure(parameters)),
        )
        return structure(response, batch_create_results.UserBonusBatchCreateResult)

    @expand('parameters')
    def create_user_bonuses_async(self, user_bonuses: List[UserBonus], parameters: Optional[UserBonusCreateRequestParameters] = None) -> operations.UserBonusCreateBatchOperation:
        params = {'async_mode': True, **(unstructure(parameters) or {})}
        response = self._request('post', '/v1/user-bonuses', json=unstructure(user_bonuses), params=params)
        return structure(response, operations.UserBonusCreateBatchOperation)

    @expand('request')
    def find_user_bonuses(self, request: search_requests.UserBonusSearchRequest,
                          sort: Union[List[str], search_requests.UserBonusSortItems, None] = None,
                          limit: Optional[int] = None) -> search_results.UserBonusSearchResult:
        sort = None if sort is None else structure(sort, search_requests.UserBonusSortItems)
        response = self._search_request('get', '/v1/user-bonuses', request, sort, limit)
        return structure(response, search_results.UserBonusSearchResult)

    def get_user_bonus(self, user_bonus_id: str) -> UserBonus:
        response = self._request('get', f'/v1/user-bonuses/{user_bonus_id}')
        return structure(response, UserBonus)

    @expand('request')
    def get_user_bonuses(self, request: search_requests.UserBonusSearchRequest) -> Generator[UserBonus, None, None]:
        return self._find_all(self.find_user_bonuses, request)

    # User restrictions

    @expand('request')
    def find_user_restrictions(self, request: search_requests.UserRestrictionSearchRequest,
                               sort: Union[List[str], search_requests.UserRestrictionSortItems, None] = None,
                               limit: Optional[int] = None) -> search_results.UserRestrictionSearchResult:
        sort = None if sort is None else structure(sort, search_requests.UserRestrictionSortItems)
        response = self._search_request('get', '/v1/user-restrictions', request, sort, limit)
        return structure(response, search_results.UserRestrictionSearchResult)

    def get_user_restriction(self, user_restriction_id: str) -> UserRestriction:
        response = self._request('get', f'/v1/user-restrictions/{user_restriction_id}')
        return structure(response, UserRestriction)

    @expand('request')
    def get_user_restrictions(self, request: search_requests.UserRestrictionSearchRequest) -> Generator[UserRestriction, None, None]:
        return self._find_all(self.find_user_restrictions, request)

    def set_user_restriction(self, user_restriction: UserRestriction) -> UserRestriction:
        response = self._request('put', '/v1/user-restrictions', json=unstructure(user_restriction))
        return structure(response, UserRestriction)

    def delete_user_restriction(self, user_restriction_id: str) -> None:
        self._raw_request('delete', f'/v1/user-restrictions/{user_restriction_id}')

    # Requester

    def get_requester(self) -> Requester:
        response = self._request('get', '/v1/requester')
        return structure(response, Requester)

    # User skills

    @expand('request')
    def find_user_skills(self, request: search_requests.UserSkillSearchRequest,
                         sort: Union[List[str], search_requests.UserSkillSortItems, None] = None,
                         limit: Optional[int] = None) -> search_results.UserSkillSearchResult:
        sort = None if sort is None else structure(sort, search_requests.UserSkillSortItems)
        response = self._search_request('get', '/v1/user-skills', request, sort, limit)
        return structure(response, search_results.UserSkillSearchResult)

    def get_user_skill(self, user_skill_id: str) -> UserSkill:
        response = self._request('get', f'/v1/user-skills/{user_skill_id}')
        return structure(response, UserSkill)

    @expand('request')
    def get_user_skills(self, request: search_requests.UserSkillSearchRequest) -> Generator[UserSkill, None, None]:
        return self._find_all(self.find_user_skills, request)

    @expand('request')
    def set_user_skill(self, request: SetUserSkillRequest) -> UserSkill:
        response = self._request('put', '/v1/user-skills', json=unstructure(request))
        return structure(response, UserSkill)

    def delete_user_skill(self, user_skill_id: str) -> None:
        self._raw_request('delete', f'/v1/user-skills/{user_skill_id}')

    @expand('parameters')
    def get_assignments_df(self, pool_id: str, parameters: GetAssignmentsTsvParameters) -> pd.DataFrame:
        logger.warning('Experimental method')
        response = self._raw_request('get', f'/new/requester/pools/{pool_id}/assignments.tsv',
                                     params=unstructure(parameters))
        return pd.read_csv(io.StringIO(response.text), delimiter='\t')
