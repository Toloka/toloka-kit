import os
import pytest

from toloka.client import TolokaClient
from toloka.client.project import Project
from toloka.client.project.task_spec import TaskSpec
from toloka.client.project.field_spec import UrlSpec, StringSpec
from toloka.client.project.view_spec import ClassicViewSpec


@pytest.fixture(scope='session')
def dummy_task_spec():
    return TaskSpec(
        input_spec={'url': UrlSpec()},
        output_spec={'label': StringSpec(allowed_values=['true', 'false'])},
        view_spec=ClassicViewSpec(markup='<dummy/>')
    )


@pytest.fixture(scope='session')
def token():
    token = os.getenv('TOLOKA_TOKEN')
    return token


@pytest.fixture(scope='session')
def client(token):
    client = TolokaClient(token, environment='PRODUCTION')
    return client


@pytest.fixture(scope='session')
def empty_project(client, dummy_task_spec):
    test_project = Project(
        public_name='Test project',
        public_description='This is test project. It should not be public.',
        task_spec=dummy_task_spec
    )
    test_project = client.create_project(test_project)
    yield test_project
    client.archive_project(test_project.id)
    assert client.get_project(test_project.id).status == Project.ProjectStatus.ARCHIVED, \
        f'Cleanup failed!!! You should check that project {test_project.id} is archived.'


@pytest.fixture(scope='session')
def project_with_pool_id():
    return '63424'


@pytest.fixture(scope='session')
def project_with_pool(client, project_with_pool_id):
    # DO NOT TRY TO ARCHIVE THIS PROJECT IN TESTS!
    project_with_pool = client.get_project(project_with_pool_id)
    return project_with_pool


@pytest.fixture(scope='session')
def pool_in_project_with_pool(client):
    return client.get_pool('29078882')
