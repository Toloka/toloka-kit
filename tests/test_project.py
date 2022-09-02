import datetime
from operator import itemgetter
from textwrap import dedent
from urllib.parse import urlparse, parse_qs

import io
import simplejson as json
import logging
import pandas as pd
import pytest
import toloka.client as client
from toloka.client.exceptions import InternalApiError, ValidationApiError, IncorrectActionsApiError
from .template_builder.test_template_builder import view_spec_map as tb_view_spec_map  # noqa: F401

from .testutils.util_functions import check_headers


@pytest.fixture
def project_map():
    return {
        'id': '10',
        'public_name': 'Choose image color',
        'public_description': 'Look at the picture and choose it\'s dominant color',
        'private_comment': 'Submitted by Joe',
        'public_instructions': '<p>\nSome complex instructions\n</p>',
        'task_spec': {
            'input_spec': {
                'image': {
                    'hidden': False,
                    'type': 'url',
                    'required': True,
                }
            },
            'output_spec': {
                'color': {
                    'hidden': False,
                    'type': 'array_string',
                    'required': True,
                    'min_size': 1,
                    'max_size': 3,
                    'allowed_values': ['orange', 'red', 'blue', 'green']
                },
                'comment': {
                    'hidden': False,
                    'type': 'string',
                    'required': False,
                    'max_length': 2048,
                }
            },
            'view_spec': {
                'settings': {
                    'showFinish': True,
                    'showFullscreen': False,
                    'showInstructions': True,
                    'showSubmit': False,
                    'showTimer': True,
                    'showTitle': False,
                    'unexpected_setting': 1024,
                },
                'type': 'classic',
                'markup': dedent('''
                <div class="grid">
                \t{{#each image}}
                \t\t{{#task class="grid_item"}}
                \t\t\t{{img src=../this width=300 height=300}}
                \t\t\t{{field type="checkbox" name="red" label="Red" hotkey="1"}}
                \t\t{{/task}}
                \t{{/each}}
                </div>
                '''),
            }
        },
        'assignments_issuing_type': 'AUTOMATED',
        'status': 'ACTIVE',
        'created': '2015-12-09T12:10:00',
    }


@pytest.fixture
def tb_project_map(project_map, tb_view_spec_map):  # noqa F811
    project_map['task_spec']['view_spec'] = tb_view_spec_map
    return project_map


def test_find_project(requests_mock, toloka_client, toloka_url, project_map):
    raw_result = {'items': [project_map], 'has_more': False}

    def find_projects(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_projects',
            'X-Low-Level-Method': 'find_projects',
        }
        check_headers(request, expected_headers)

        assert {
            'status': ['ACTIVE'],
            'limit': ['50'],
            'sort': ['-public_name,id'],
            'id_gt': ['123'],
            'created_lt': ['2015-12-09T12:10:00'],
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(f'{toloka_url}/projects', headers={'Authorization': 'OAuth abc'}, json=find_projects, status_code=200)

    # Request object syntax
    request = client.search_requests.ProjectSearchRequest(
        status=client.Project.ProjectStatus.ACTIVE,
        id_gt='123',
        created_lt=datetime.datetime(2015, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
    )
    sort = client.search_requests.ProjectSortItems(['-public_name', 'id'])
    result = toloka_client.find_projects(request, sort=sort, limit=50)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_projects(
        status=client.Project.ProjectStatus.ACTIVE,
        id_gt='123',
        created_lt=datetime.datetime(2015, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
        limit=50,
        sort=['-public_name', 'id']
    )
    assert raw_result == client.unstructure(result)


def test_get_projects(requests_mock, toloka_client, toloka_url, project_map):
    projects = [dict(project_map, id=str(i)) for i in range(100, 200)]
    projects.sort(key=itemgetter('id'))
    expected_projects = [project for project in projects if project['id'] > '123']

    def get_projects(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_projects',
            'X-Low-Level-Method': 'find_projects',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0]
        assert {
            'status': ['ACTIVE'],
            'sort': ['id'],
            'created_lt': ['2015-12-09T12:10:00'],
        } == params

        items = [project for project in projects if project['id'] > id_gt][:3]
        return {'items': items, 'has_more': items[-1]['id'] != projects[-1]['id']}

    requests_mock.get(f'{toloka_url}/projects', headers={'Authorization': 'OAuth abc'}, json=get_projects)

    # Request object syntax
    request = client.search_requests.ProjectSearchRequest(
        status=client.Project.ProjectStatus.ACTIVE,
        id_gt='123',
        created_lt=datetime.datetime(2015, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
    )
    result = toloka_client.get_projects(request)
    assert expected_projects == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_projects(
        status=client.Project.ProjectStatus.ACTIVE,
        id_gt='123',
        created_lt=datetime.datetime(2015, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
    )
    assert expected_projects == client.unstructure(list(result))


def test_get_project(requests_mock, toloka_client, toloka_url, project_map):

    def get_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_project',
            'X-Low-Level-Method': 'get_project',
        }
        check_headers(request, expected_headers)

        return project_map

    requests_mock.get(f'{toloka_url}/projects/10', headers={'Authorization': 'OAuth abc'}, json=get_project, status_code=200)
    result = toloka_client.get_project('10')
    assert project_map == client.unstructure(result)


def test_get_project_returns_internal_server_error(requests_mock, toloka_client, toloka_url):
    body = {
        'code': 'INTERNAL_ERROR',
        'request_id': 'abc',
        'message': 'Internal Error',
        'payload': {
            'additional_message': 'Error details',
        },
    }

    def get_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_project',
            'X-Low-Level-Method': 'get_project',
        }
        check_headers(request, expected_headers)

        return body

    requests_mock.get(f'{toloka_url}/projects/10', headers={'Authorization': 'OAuth abc'}, json=get_project, status_code=500)
    with pytest.raises(InternalApiError) as excinfo:
        toloka_client.get_project('10')
    assert excinfo.value.status_code == 500
    for key, value in body.items():
        assert getattr(excinfo.value, key) == value


@pytest.fixture
def simple_poject_map():
    return {
        'id': 10,
        'public_name': 'Map Task',
        'public_description': 'Simple map task',
        'public_instructions': 'Check if company exists',
        'task_spec': {
            'input_spec': {
                'point': {
                    'type': 'coordinates',
                    'required': True,
                },
                'company': {
                    'type': 'string',
                    'required': True,
                }
            },
            'output_spec': {
                'exists': {
                    'type': 'boolean',
                    'required': True,
                }
            },
            'view_spec': {
                'markup': '<dummy/>',
                'type': 'classic',
            }
        },
        'assignments_issuing_type': 'MAP_SELECTOR',
        'assignments_issuing_view_config': {
            'title_template': 'Company: {{inputParams[\'company\']}}',
            'description_template': 'Check if company {{inputParams[\'company\']}} exists',
            'map_provider': 'YANDEX',
        },
        'metadata': {'projectMetadataKey': ['projectMetadataValue']},
        'quality_control': {
            'config': [
                {
                    'collector_config': {
                        'type': 'ANSWER_COUNT',
                        'uuid': 'daab2575-374a-4006-b285-9760db09795c',
                    },
                    'rules': [
                        {
                            'action': {
                                'type': 'RESTRICTION',
                                'parameters': {
                                    'scope': 'POOL'
                                }
                            },
                            'conditions': [
                                {
                                    'key': 'assignments_accepted_count',
                                    'value': 42000,
                                    'operator': 'GTE',
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        'assignments_automerge_enabled': True,
        'status': 'ACTIVE',
        'created': '2015-12-09T12:10:00',
    }


def test_create_project(requests_mock, toloka_client, toloka_url, simple_poject_map, caplog):

    def project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_project',
            'X-Low-Level-Method': 'create_project',
        }
        check_headers(request, expected_headers)

        return simple_poject_map

    requests_mock.post(f'{toloka_url}/projects', headers={'Content-Type': 'application/json; charset=UTF-8'}, json=project, status_code=201)

    project = client.structure(simple_poject_map, client.project.Project)
    with caplog.at_level(logging.INFO):
        caplog.clear()
        result = toloka_client.create_project(project)
        assert caplog.record_tuples == [(
            'toloka.client', logging.INFO,
            'A new project with ID "10" has been created. Link to open in web interface: https://sandbox.toloka.yandex.com/requester/project/10'
        )]
        assert project == result


def test_create_project_check_validation_errors(requests_mock, toloka_client, toloka_url):
    body = {
        'public_name': 'Map Task',
        'task_spec': {
            'input_spec': {'input': {'type': 'boolean', 'required': True, 'hidden': False}},
            'output_spec': {'output': {'type': 'boolean', 'required': True, 'hidden': False}},
            'view_spec': {'type': 'classic', 'markup': '<dummy/>'}
        },
        'assignments_issuing_type': 'AUTOMATED',
    }

    response_body = {
        'code': 'VALIDATION_ERROR',
        'message': 'Validation error',
        'request_id': 'abc-123',
        'payload': {
            'public_description': {
                'code': 'VALUE_REQUIRED',
                'message': 'Value must be present',
            },
            'task_spec': {
                'code': 'OBJECT_EXPECTED',
                'message': 'Value must be an object',
            },
        },
    }

    def create_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_project',
            'X-Low-Level-Method': 'create_project',
        }
        check_headers(request, expected_headers)

        assert body == request.json()
        return response_body

    requests_mock.post(f'{toloka_url}/projects', headers={'Content-Type': 'application/json; charset=UTF-8'}, json=create_project, status_code=400)

    project = client.project.Project(
        public_name='Map Task',
        public_description=None,
        task_spec=client.project.task_spec.TaskSpec(
            input_spec={'input': client.project.field_spec.BooleanSpec(required=True)},
            output_spec={'output': client.project.field_spec.BooleanSpec(required=True)},
            view_spec=client.project.view_spec.ClassicViewSpec(markup='<dummy/>')
        ),
        assignments_issuing_type=client.project.Project.AssignmentsIssuingType.AUTOMATED,
        public_instructions=None
    )

    with pytest.raises(ValidationApiError) as excinfo:
        toloka_client.create_project(project)
    assert excinfo.value.status_code == 400
    for key, value in response_body.items():
        assert getattr(excinfo.value, key) == value
    assert excinfo.value.invalid_fields == list(response_body['payload'].keys())


def test_create_project_check_logical_errors(requests_mock, toloka_client, toloka_url):
    body = {
        'public_name': 'Map Task',
        'task_spec': {
            'input_spec': {'input': {'type': 'boolean', 'required': True, 'hidden': False}},
            'output_spec': {'output': {'type': 'boolean', 'required': True, 'hidden': False}},
            'view_spec': {'type': 'classic', 'markup': '<dummy/>'}
        },
        'assignments_issuing_type': 'AUTOMATED',
    }

    response_body = {
        'code': 'NEED_PHONE_CONFIRMATION',
        'message': 'Need phone confirmation',
        'request_id': 'abc-123',
    }

    def create_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_project',
            'X-Low-Level-Method': 'create_project',
        }
        check_headers(request, expected_headers)

        assert body == request.json()
        return response_body

    requests_mock.post(f'{toloka_url}/projects', headers={'Content-Type': 'application/json; charset=UTF-8'}, json=create_project, status_code=400)

    project = client.project.Project(
        public_name='Map Task',
        public_description=None,
        task_spec=client.project.task_spec.TaskSpec(
            input_spec={'input': client.project.field_spec.BooleanSpec(required=True)},
            output_spec={'output': client.project.field_spec.BooleanSpec(required=True)},
            view_spec=client.project.view_spec.ClassicViewSpec(markup='<dummy/>')
        ),
        assignments_issuing_type=client.project.Project.AssignmentsIssuingType.AUTOMATED,
        public_instructions=None
    )

    with pytest.raises(IncorrectActionsApiError) as excinfo:
        toloka_client.create_project(project)
    assert excinfo.value.status_code == 400
    for key, value in response_body.items():
        assert getattr(excinfo.value, key) == value


def test_project_update(requests_mock, toloka_client, toloka_url):
    project_map = {
        'public_name': 'Map Task',
        'public_description': 'Simple map task',
        'public_instructions': 'Check if company exists',
        'task_spec': {
            'input_spec': {
                'point': {
                    'type': 'coordinates',
                    'required': True,
                    'hidden': False,
                },
                'company': {
                    'type': 'string',
                    'required': True,
                    'hidden': False,
                }
            },
            'output_spec': {
                'exists': {
                    'type': 'boolean',
                    'required': True,
                    'hidden': False,
                }
            },
            'view_spec': {
                'markup': '<dummy/>',
                'type': 'classic',
            }
        },
        'assignments_issuing_type': 'MAP_SELECTOR',
        'max_active_assignments_count': 5,
        'assignments_issuing_view_config': {
            'title_template': 'Company: {{inputParams[\'company\']}}',
            'description_template': 'Check if company {{inputParams[\'company\']}} exists',
            'map_provider': 'GOOGLE'
        },
    }

    def update_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'update_project',
            'X-Low-Level-Method': 'update_project',
        }
        check_headers(request, expected_headers)

        assert project_map == request.json()
        return dict(
            project_map,
            status='ACTIVE',
            created='2015-12-09T12:10:00',
            max_active_assignments_count=5,
            id='10',
        )

    requests_mock.put(f'{toloka_url}/projects/10', headers={'Content-Type': 'application/json; charset=UTF-8'}, json=update_project, status_code=200)
    update_to_project = client.project.Project(
        public_name='Map Task',
        public_description='Simple map task',
        task_spec=client.project.task_spec.TaskSpec(
            input_spec={
                'point': client.project.field_spec.CoordinatesSpec(required=True),
                'company': client.project.field_spec.StringSpec(required=True),
            },
            output_spec={'exists': client.project.field_spec.BooleanSpec(required=True)},
            view_spec=client.project.view_spec.ClassicViewSpec(markup='<dummy/>'),
        ),
        assignments_issuing_type=client.project.Project.AssignmentsIssuingType.MAP_SELECTOR,
        public_instructions='Check if company exists',
        assignments_issuing_view_config=client.project.Project.AssignmentsIssuingViewConfig(
            title_template='Company: {{inputParams[\'company\']}}',
            description_template='Check if company {{inputParams[\'company\']}} exists',
            map_provider=client.project.Project.AssignmentsIssuingViewConfig.MapProvider.GOOGLE
        ),
        max_active_assignments_count=5
    )

    project = client.project.Project(
        public_name='Map Task',
        public_description='Simple map task',
        task_spec=client.project.task_spec.TaskSpec(
            input_spec={
                'point': client.project.field_spec.CoordinatesSpec(required=True),
                'company': client.project.field_spec.StringSpec(required=True),
            },
            output_spec={'exists': client.project.field_spec.BooleanSpec(required=True)},
            view_spec=client.project.view_spec.ClassicViewSpec(markup='<dummy/>')
        ),
        assignments_issuing_type=client.project.Project.AssignmentsIssuingType.MAP_SELECTOR,
        public_instructions='Check if company exists',
        assignments_issuing_view_config=client.project.Project.AssignmentsIssuingViewConfig(
            title_template='Company: {{inputParams[\'company\']}}',
            description_template='Check if company {{inputParams[\'company\']}} exists',
            map_provider=client.project.Project.AssignmentsIssuingViewConfig.MapProvider.GOOGLE
        ),
        max_active_assignments_count=5,
        id='10',
        status=client.project.Project.ProjectStatus.ACTIVE,
        created=datetime.datetime(2015, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
    )

    result = toloka_client.update_project('10', update_to_project)
    assert result == project


def test_project_from_json(project_map):
    project = client.structure(project_map, client.project.Project)
    project_json = json.dumps(project_map, use_decimal=True, ensure_ascii=False)
    project_from_json = client.project.Project.from_json(project_json)
    assert project == project_from_json


def test_project_to_json(project_map):
    project = client.structure(project_map, client.project.Project)
    project_json = project.to_json()
    project_json_basic = json.dumps(project_map, use_decimal=True, ensure_ascii=False)
    assert json.loads(project_json) == json.loads(project_json_basic)


@pytest.fixture
def archive_operation_map():
    return {
        'id': 'archive-project-op-1',
        'type': 'PROJECT.ARCHIVE',
        'status': 'RUNNING',
        'submitted': '2016-10-21T15:37:00',
        'started': '2016-10-21T15:37:01',
        'finished': '2016-10-21T15:37:02',
        'parameters': {
            'project_id': '10',
        },
    }


@pytest.fixture
def complete_archive_operation_map(archive_operation_map):
    return {
        **archive_operation_map,
        'status': 'SUCCESS',
        'finished': '2016-03-07T15:48:03',
    }


def test_archive_project_async(requests_mock, toloka_client, toloka_url, complete_archive_operation_map):

    def complete_archive(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'archive_project_async',
            'X-Low-Level-Method': 'archive_project_async',
        }
        check_headers(request, expected_headers)

        return complete_archive_operation_map

    requests_mock.post(f'{toloka_url}/projects/10/archive', json=complete_archive, status_code=202)
    result = toloka_client.archive_project_async('10')
    assert complete_archive_operation_map == client.unstructure(result)


def test_archive_project(requests_mock, toloka_client, toloka_url,
                         archive_operation_map, complete_archive_operation_map, project_map):

    def archive(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'archive_project',
            'X-Low-Level-Method': 'archive_project_async',
        }
        check_headers(request, expected_headers)

        return archive_operation_map

    def complete_archive(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'archive_project',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return complete_archive_operation_map

    def project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'archive_project',
            'X-Low-Level-Method': 'get_project',
        }
        check_headers(request, expected_headers)

        return project_map

    requests_mock.post(f'{toloka_url}/projects/10/archive', json=archive, status_code=202)
    requests_mock.get(
        f'{toloka_url}/operations/{archive_operation_map["id"]}',
        json=complete_archive,
        status_code=200
    )
    requests_mock.get(f'{toloka_url}/projects/10', json=project, status_code=200)

    result = toloka_client.archive_project('10')
    assert project_map == client.unstructure(result)


def test_get_template_builder_project(requests_mock, toloka_client, toloka_url, tb_project_map):

    def tb_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_project',
            'X-Low-Level-Method': 'get_project',
        }
        check_headers(request, expected_headers)

        return tb_project_map

    requests_mock.get(f'{toloka_url}/projects/10', headers={'Authorization': 'OAuth abc'}, json=tb_project, status_code=200)
    result = toloka_client.get_project('10')
    unstructured_result = client.unstructure(result)
    expected_template_config = tb_project_map['task_spec']['view_spec'].pop('config')
    real_template_config = unstructured_result.get('task_spec', {}).get('view_spec', {'config': None}).pop('config')
    assert real_template_config
    assert json.loads(expected_template_config) == json.loads(real_template_config)
    assert tb_project_map == unstructured_result


def test_get_assignments_df(requests_mock, toloka_client, toloka_api_url):
    # urllib.parse.parse_qs format
    expected_params = {
        'status': [','.join([str.lower(s.value) for s in client.assignment.GetAssignmentsTsvParameters.Status])],
        'starttimefrom': ['2020-01-01t00:00:00'],
        'excludebanned': ['true'],
        'addrowdelimiter': ['false'],
        'field': [','.join([str.lower(f.value) for f in client.assignment.GetAssignmentsTsvParameters._default_fields])],
    }
    expected_df = pd.DataFrame(data={
        'a': [1, 2, 3],
        'b': [4, 5, 6]
    })
    buf = io.StringIO()
    expected_df.to_csv(buf, sep='\t', index=False, columns=['a', 'b'])

    def get_content(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_assignments_df',
            'X-Low-Level-Method': 'get_assignments_df',
        }
        check_headers(request, expected_headers)

        return buf.getvalue().encode('utf-8')

    requests_mock.get(f'{toloka_api_url}/new/requester/pools/123/assignments.tsv',
                      content=get_content,
                      headers={'Authorization': 'OAuth abc'},
                      status_code=200)
    result = toloka_client.get_assignments_df(
        pool_id='123',
        parameters=client.assignment.GetAssignmentsTsvParameters(
            start_time_from=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
            exclude_banned=True,
            status=[s for s in client.assignment.GetAssignmentsTsvParameters.Status]
        )
    )

    assert result.equals(expected_df)
    assert requests_mock.last_request.qs == expected_params

    result = toloka_client.get_assignments_df(
        pool_id='123', start_time_from=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
        exclude_banned=True, status=[s for s in client.assignment.GetAssignmentsTsvParameters.Status]
    )

    assert result.equals(expected_df)
    assert requests_mock.last_request.qs == expected_params


@pytest.fixture
def simple_localization_config_map():
    return {
        'default_language': 'RU',
        'additional_languages':
        [
            {
                'language': 'EN',
                'public_name':
                {
                    'value': 'English Project Name',
                    'source': 'REQUESTER',
                },
                'public_description':
                {
                    'value': 'Project Description',
                    'source': 'REQUESTER',
                },
                'public_instructions':
                {
                    'value': 'Project Instructions',
                    'source': 'REQUESTER',
                },
            },
        ],
    }


@pytest.fixture
def project_map_with_localization(project_map, simple_localization_config_map):
    return {
        **project_map,
        'localization_config': simple_localization_config_map,
    }


def test_localization(requests_mock, toloka_client, toloka_url, project_map, project_map_with_localization):

    def project_with_localization(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_project',
            'X-Low-Level-Method': 'create_project',
        }
        check_headers(request, expected_headers)

        return project_map_with_localization

    requests_mock.post(f'{toloka_url}/projects', headers={'Content-Type': 'application/json; charset=UTF-8'}, json=project_with_localization, status_code=201)

    project = client.structure(project_map, client.project.Project)

    project.localization_config = client.project.LocalizationConfig(
        default_language='RU',
        additional_languages=[
            client.project.AdditionalLanguage(
                language='EN',
                public_name=client.project.AdditionalLanguage.FieldTranslation(
                    value='Project name',
                    source='REQUESTER',
                ),
                public_description=client.project.AdditionalLanguage.FieldTranslation(
                    value='Translated description',
                    source='REQUESTER',
                ),
                public_instructions=client.project.AdditionalLanguage.FieldTranslation(
                    value='Translated instruction',
                    source='REQUESTER',
                ),
            )
        ]
    )

    result = toloka_client.create_project(project)
    assert project_map_with_localization == client.unstructure(result)


def test_localization_funcs(project_map):
    project1 = client.structure(project_map, client.project.Project)

    project1.localization_config = client.project.LocalizationConfig(
        default_language='RU',
        additional_languages=[
            client.project.AdditionalLanguage(
                language='EN',
                public_name=client.project.AdditionalLanguage.FieldTranslation(
                    value='Project name',
                    source='REQUESTER',
                ),
                public_description=client.project.AdditionalLanguage.FieldTranslation(
                    value='Translated description',
                    source='REQUESTER',
                ),
                public_instructions=client.project.AdditionalLanguage.FieldTranslation(
                    value='Translated instruction',
                    source='REQUESTER',
                ),
            )
        ]
    )

    project2 = client.structure(project_map, client.project.Project)
    project2.set_default_language('RU')
    project2.add_requester_translation(
        'EN',
        public_name='Project name',
        public_description='Translated description',
        public_instructions='Translated instruction',
    )
    assert client.unstructure(project1) == client.unstructure(project2)

    project3 = client.structure(project_map, client.project.Project)
    project3.add_requester_translation(
        'EN',
        public_name='Project name',
        public_description='Translated description',
        public_instructions='Translated instruction',
    )
    project3.set_default_language('RU')
    assert client.unstructure(project1) == client.unstructure(project3)

    project4 = client.structure(project_map, client.project.Project)
    project4.add_requester_translation(
        'EN',
        public_name='',
        public_description='',
        public_instructions='',
    )
    project4.set_default_language('RU')
    project4.add_requester_translation(
        'EN',
        public_name='Project name',
        public_description='Translated description',
        public_instructions='Translated instruction',
    )
    assert client.unstructure(project1) == client.unstructure(project4)

    project5 = client.structure(project_map, client.project.Project)
    project5.set_default_language('RU')
    project5.add_requester_translation(language='EN', public_name='Project name')
    project5.add_requester_translation(language='EN', public_description='Translated description')
    project5.add_requester_translation(language='EN', public_instructions='Translated instruction')
    assert client.unstructure(project1) == client.unstructure(project5)
