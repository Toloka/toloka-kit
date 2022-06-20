import asyncio
import datetime

import pytest
from toloka.client.project import Project
from ..template_builder import compare_view_specs
from toloka.metrics import TasksInPool


def test_project_is_created(client, empty_project):
    assert client.get_project(empty_project.id).status == Project.ProjectStatus.ACTIVE


def test_get_project(project_with_pool, project_with_pool_id):
    assert project_with_pool.id == project_with_pool_id


@pytest.fixture
def cloned_project_with_pool(client, project_with_pool):
    clone_result = client.clone_project(project_with_pool.id)
    cloned_project, cloned_pools = clone_result.project, clone_result.pools
    yield cloned_project
    for pool in cloned_pools:
        client.archive_pool(pool.id)
    client.archive_project(cloned_project.id)
    assert client.get_project(cloned_project.id).status == Project.ProjectStatus.ARCHIVED, \
        f'Cleanup failed!!! You should check that project {cloned_project.id} is archived.'


def test_clone_project(cloned_project_with_pool, project_with_pool):
    for (key1, value1), (key2, value2) in zip(
        sorted(cloned_project_with_pool.unstructure().items()),
        sorted(project_with_pool.unstructure().items())
    ):
        if key1 not in {'status', 'created', 'id'}:
            if key1 == 'task_spec':
                compare_view_specs(value1['view_spec'], value2['view_spec'])
                value1.pop('view_spec')
                value2.pop('view_spec')
            assert value1 == value2, f'Projects are different in {key1}'


def test_project_is_findable(client, project_with_pool):
    found_project = client.find_projects(id_lte=project_with_pool.id, id_gte=project_with_pool.id).items[0]
    assert found_project == project_with_pool


def test_project_is_gettable(client, project_with_pool):
    got_project = next(client.get_projects(id_lte=project_with_pool.id, id_gte=project_with_pool.id))
    assert got_project == project_with_pool


def test_update_project(client, cloned_project_with_pool):
    cloned_project_with_pool.public_name = 'Updated public name'
    client.update_project(cloned_project_with_pool.id, cloned_project_with_pool)
    assert client.get_project(cloned_project_with_pool.id).public_name == 'Updated public name'


def test_metrics_time_format(client, pool_in_project_with_pool):
    lines = asyncio.run(TasksInPool(pool_in_project_with_pool.id, tasks_name='test', toloka_client=client).get_lines())
    assert lines['test'][0][0].tzinfo == datetime.timezone.utc
