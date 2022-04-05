import datetime
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import simplejson
import toloka.client as client

from ..testutils.util_functions import check_headers


def test_find_apps(requests_mock, toloka_client_prod, toloka_app_url, app_map):
    raw_result = {'content': [app_map], 'has_more': False}

    def apps(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_apps',
            'X-Low-Level-Method': 'find_apps',
        }
        check_headers(request, expected_headers)

        assert {
            'after_id': ['123'],
            'sort': ['name,-id'],
        } == parse_qs(urlparse(request.url).query)
        return simplejson.dumps(raw_result)

    requests_mock.get(f'{toloka_app_url}/apps', text=apps)

    # Request object syntax
    request = client.search_requests.AppSearchRequest(
        after_id='123',
    )
    sort = client.search_requests.AppSortItems(['name', '-id'])
    result = toloka_client_prod.find_apps(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client_prod.find_apps(
        after_id='123',
        sort=['name', '-id'],
    )
    assert raw_result == client.unstructure(result)


def test_get_apps(requests_mock, toloka_client_prod, toloka_app_url, app_map):
    apps = [dict(app_map, id=str(i)) for i in range(100)]
    apps.sort(key=itemgetter('id'))
    expected_apps = [app for app in apps if app['id'] > '20']

    def get_apps(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_apps',
            'X-Low-Level-Method': 'find_apps',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0]
        assert {
            'sort': ['id'],
            'name_gt': ['name']
        } == params

        items = [app for app in apps if id_gt is None or app['id'] > id_gt][:3]
        return simplejson.dumps({'content': items, 'has_more': items[-1]['id'] != apps[-1]['id']})

    requests_mock.get(f'{toloka_app_url}/apps', text=get_apps)

    # Request object syntax
    request = client.search_requests.AppSearchRequest(
        id_gt='20',
        name_gt='name'
    )
    result = toloka_client_prod.get_apps(request)
    assert expected_apps == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client_prod.get_apps(
        id_gt='20',
        name_gt='name'
    )
    assert expected_apps == client.unstructure(list(result))


def test_get_apps_one_params(requests_mock, toloka_client_prod, toloka_app_url, app_map):
    apps = [dict(app_map, id=str(i)) for i in range(10)]
    apps.sort(key=itemgetter('id'))
    expected_apps = [app for app in apps]

    def get_apps(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_apps',
            'X-Low-Level-Method': 'find_apps',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        assert {'after_id': ['1'], 'sort': ['id']} == params
        return simplejson.dumps({'content': [app for app in apps], 'has_more': False})

    requests_mock.get(f'{toloka_app_url}/apps', text=get_apps)

    # Expanded positional syntax
    result = toloka_client_prod.get_apps(after_id='1')
    assert expected_apps == client.unstructure(list(result))


def test_get_app(requests_mock, toloka_client_prod, toloka_app_url, app_map):

    def get_app(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app',
            'X-Low-Level-Method': 'get_app',
        }
        check_headers(request, expected_headers)

        return simplejson.dumps(app_map)

    requests_mock.get(f'{toloka_app_url}/apps/21', text=get_app)
    assert app_map == client.unstructure(toloka_client_prod.get_app('21'))


def test_find_app_projects(requests_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):
    raw_result = {'content': [app_project_map_with_readonly], 'has_more': False}

    def app_projects(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_app_projects',
            'X-Low-Level-Method': 'find_app_projects',
        }
        check_headers(request, expected_headers)

        assert {
            'app_id': ['123'],
            'sort': ['name,-id'],
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(f'{toloka_app_url}/app-projects', json=app_projects)

    # Request object syntax
    request = client.search_requests.AppProjectSearchRequest(
        app_id='123',
    )
    sort = client.search_requests.AppProjectSortItems(['name', '-id'])
    result = toloka_client_prod.find_app_projects(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client_prod.find_app_projects(
        app_id='123',
        sort=['name', '-id'],
    )
    assert raw_result == client.unstructure(result)


def test_get_app_projects(requests_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):
    app_projects = [dict(app_project_map_with_readonly, id=str(i)) for i in range(100)]
    app_projects.sort(key=itemgetter('id'))
    expected_app_projects = [project for project in app_projects if project['id'] > '20']

    def get_app_projects(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_projects',
            'X-Low-Level-Method': 'find_app_projects',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0]
        assert {
            'sort': ['id'],
            'created_gt':  ['2016-03-23T12:59:00']
        } == params

        items = [project for project in app_projects if id_gt is None or project['id'] > id_gt][:3]
        return {'content': items, 'has_more': items[-1]['id'] != app_projects[-1]['id']}

    requests_mock.get(f'{toloka_app_url}/app-projects', json=get_app_projects)

    # Request object syntax
    request = client.search_requests.AppProjectSearchRequest(
        id_gt='20',
        created_gt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc)
    )
    result = toloka_client_prod.get_app_projects(request)
    assert expected_app_projects == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client_prod.get_app_projects(
        id_gt='20',
        created_gt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc)
    )
    assert expected_app_projects == client.unstructure(list(result))


def test_get_app_projects_one_params(requests_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):
    app_projects = [dict(app_project_map_with_readonly, id=str(i)) for i in range(10)]
    app_projects.sort(key=itemgetter('id'))
    expected_app_projects = [project for project in app_projects]

    def get_app_projects(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_projects',
            'X-Low-Level-Method': 'find_app_projects',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        assert {'status': ['READY'], 'sort': ['id']} == params
        return {'content': [project for project in app_projects], 'has_more': False}

    requests_mock.get(f'{toloka_app_url}/app-projects', json=get_app_projects)

    # Expanded positional syntax
    result = toloka_client_prod.get_app_projects(status='READY')
    assert expected_app_projects == client.unstructure(list(result))


def test_get_app_project(requests_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):

    def get_app_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_project',
            'X-Low-Level-Method': 'get_app_project',
        }
        check_headers(request, expected_headers)

        return app_project_map_with_readonly

    requests_mock.get(f'{toloka_app_url}/app-projects/123', json=get_app_project)
    assert app_project_map_with_readonly == client.unstructure(toloka_client_prod.get_app_project('123'))


def test_create_app_project(requests_mock, toloka_client_prod, toloka_app_url, app_map, app_project_map_with_readonly):

    def app_projects(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_app_project',
            'X-Low-Level-Method': 'create_app_project',
        }
        check_headers(request, expected_headers)

        assert app_map == request.json()
        return app_project_map_with_readonly

    requests_mock.post(f'{toloka_app_url}/app-projects', json=app_projects, status_code=201)
    app_project = client.structure(app_map, client.app.App)
    result = toloka_client_prod.create_app_project(app_project)
    assert app_project_map_with_readonly == client.unstructure(result)


def test_archive_app_project(requests_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):

    def archive_app_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'archive_app_project',
            'X-Low-Level-Method': 'archive_app_project',
        }
        check_headers(request, expected_headers)

        return app_project_map_with_readonly

    def get_app_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'archive_app_project',
            'X-Low-Level-Method': 'get_app_project',
        }
        check_headers(request, expected_headers)

        return app_project_map_with_readonly

    requests_mock.post(f'{toloka_app_url}/app-projects/123/archive', json=archive_app_project)
    requests_mock.get(f'{toloka_app_url}/app-projects/123', json=get_app_project)
    assert app_project_map_with_readonly == client.unstructure(toloka_client_prod.archive_app_project('123'))


def test_unarchive_app_project(requests_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):

    def unarchive_app_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'unarchive_app_project',
            'X-Low-Level-Method': 'unarchive_app_project',
        }
        check_headers(request, expected_headers)

        return app_project_map_with_readonly

    def get_app_project(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'unarchive_app_project',
            'X-Low-Level-Method': 'get_app_project',
        }
        check_headers(request, expected_headers)

        return app_project_map_with_readonly

    requests_mock.post(f'{toloka_app_url}/app-projects/123/unarchive', json=unarchive_app_project)
    requests_mock.get(f'{toloka_app_url}/app-projects/123', json=get_app_project)
    assert app_project_map_with_readonly == client.unstructure(toloka_client_prod.unarchive_app_project('123'))


def test_find_app_items(requests_mock, toloka_client_prod, toloka_app_url, app_item_map_with_readonly):
    raw_result = {'content': [app_item_map_with_readonly], 'has_more': False}

    def app_items(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_app_items',
            'X-Low-Level-Method': 'find_app_items',
        }
        check_headers(request, expected_headers)

        assert {
            'after_id': ['123'],
            'sort': ['created_at,-id'],
        } == parse_qs(urlparse(request.url).query)
        return simplejson.dumps(raw_result)

    requests_mock.get(f'{toloka_app_url}/app-projects/123/items', text=app_items)

    # Request object syntax
    request = client.search_requests.AppItemSearchRequest(
        after_id='123',
    )
    sort = client.search_requests.AppItemSortItems(['created_at', '-id'])
    result = toloka_client_prod.find_app_items('123', request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client_prod.find_app_items(
        '123',
        after_id='123',
        sort=['created_at', '-id'],
    )
    assert raw_result == client.unstructure(result)


def test_get_app_items(requests_mock, toloka_client_prod, toloka_app_url, app_item_map_with_readonly):
    app_items = [dict(app_item_map_with_readonly, id=str(i)) for i in range(100)]
    app_items.sort(key=itemgetter('id'))
    expected_app_items = [app_item for app_item in app_items if app_item['id'] > '20']

    def get_app_items(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_items',
            'X-Low-Level-Method': 'find_app_items',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0]
        assert {
            'sort': ['id'],
            'created_at_gt':  ['2016-03-23T12:59:00']
        } == params

        items = [app_item for app_item in app_items if id_gt is None or app_item['id'] > id_gt][:3]
        return simplejson.dumps({'content': items, 'has_more': items[-1]['id'] != app_items[-1]['id']})

    requests_mock.get(f'{toloka_app_url}/app-projects/123/items', text=get_app_items)

    # Request object syntax
    request = client.search_requests.AppItemSearchRequest(
        id_gt='20',
        created_at_gt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc)
    )
    result = toloka_client_prod.get_app_items('123', request)
    assert expected_app_items == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client_prod.get_app_items(
        '123',
        id_gt='20',
        created_at_gt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc)
    )
    assert expected_app_items == client.unstructure(list(result))


def test_get_app_items_one_params(requests_mock, toloka_client_prod, toloka_app_url, app_item_map_with_readonly):
    app_items = [dict(app_item_map_with_readonly, id=str(i)) for i in range(10)]
    app_items.sort(key=itemgetter('id'))
    expected_app_items = [app_item for app_item in app_items]

    def get_app_items(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_items',
            'X-Low-Level-Method': 'find_app_items',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        assert {'after_id': ['1'], 'sort': ['id']} == params
        return simplejson.dumps({'content': [app_item for app_item in app_items], 'has_more': False})

    requests_mock.get(f'{toloka_app_url}/app-projects/123/items', text=get_app_items)

    # Expanded positional syntax
    result = toloka_client_prod.get_app_items('123', after_id='1')
    assert expected_app_items == client.unstructure(list(result))


def test_get_app_item(requests_mock, toloka_client_prod, toloka_app_url, app_item_map_with_readonly):

    def get_app_item(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_item',
            'X-Low-Level-Method': 'get_app_item',
        }
        check_headers(request, expected_headers)

        return simplejson.dumps(app_item_map_with_readonly)

    requests_mock.get(f'{toloka_app_url}/app-projects/21/items/123', text=get_app_item)
    assert app_item_map_with_readonly == client.unstructure(toloka_client_prod.get_app_item('21', '123'))


def test_create_app_item(requests_mock, toloka_client_prod, toloka_app_url, app_item_map, app_item_map_with_readonly):

    def app_items(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_app_item',
            'X-Low-Level-Method': 'create_app_item',
        }
        check_headers(request, expected_headers)

        assert app_item_map == request.json()
        return simplejson.dumps(app_item_map_with_readonly)

    requests_mock.post(f'{toloka_app_url}/app-projects/123/items', text=app_items, status_code=201)
    app_item = client.structure(app_item_map, client.app.AppItem)
    result = toloka_client_prod.create_app_item('123', app_item)
    assert app_item_map_with_readonly == client.unstructure(result)


def test_create_app_items(requests_mock, toloka_client_prod, toloka_app_url, app_item_map, app_item_map_with_readonly):

    app_items_create_request = {
        'batch_id': app_item_map['batch_id'],
        'items': [app_item_map['input_data']]
    }

    def app_items(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_app_items',
            'X-Low-Level-Method': 'create_app_items',
        }
        check_headers(request, expected_headers)

        assert app_items_create_request == request.json()
        return

    requests_mock.post(f'{toloka_app_url}/app-projects/123/items/bulk', json=app_items, status_code=201)
    app_item = client.structure(app_items_create_request, client.app.AppItemsCreateRequest)
    toloka_client_prod.create_app_items('123', app_item)


def test_find_app_batches(requests_mock, toloka_client_prod, toloka_app_url, app_batch_map):
    raw_result = {'content': [app_batch_map], 'has_more': False}

    def app_batches(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_app_batches',
            'X-Low-Level-Method': 'find_app_batches',
        }
        check_headers(request, expected_headers)

        assert {
            'after_id': ['123'],
            'sort': ['created_at,-id'],
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(f'{toloka_app_url}/app-projects/123/batches', json=app_batches)

    # Request object syntax
    request = client.search_requests.AppBatchSearchRequest(
        after_id='123',
    )
    sort = client.search_requests.AppBatchSortItems(['created_at', '-id'])
    result = toloka_client_prod.find_app_batches('123', request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client_prod.find_app_batches(
        '123',
        after_id='123',
        sort=['created_at', '-id'],
    )
    assert raw_result == client.unstructure(result)


def test_get_app_batches(requests_mock, toloka_client_prod, toloka_app_url, app_batch_map):
    app_batches = [dict(app_batch_map, id=str(i)) for i in range(100)]
    app_batches.sort(key=itemgetter('id'))
    expected_app_batches = [app_batch for app_batch in app_batches if app_batch['id'] > '20']

    def get_app_batches(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_batches',
            'X-Low-Level-Method': 'find_app_batches',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0]
        assert {
            'sort': ['id'],
            'name_gt': ['name']
        } == params

        items = [app_batch for app_batch in app_batches if id_gt is None or app_batch['id'] > id_gt][:3]
        return {'content': items, 'has_more': items[-1]['id'] != app_batches[-1]['id']}

    requests_mock.get(f'{toloka_app_url}/app-projects/123/batches', json=get_app_batches)

    # Request object syntax
    request = client.search_requests.AppBatchSearchRequest(
        id_gt='20',
        name_gt='name'
    )
    result = toloka_client_prod.get_app_batches('123', request)
    assert expected_app_batches == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client_prod.get_app_batches(
        '123',
        id_gt='20',
        name_gt='name'
    )
    assert expected_app_batches == client.unstructure(list(result))


def test_get_app_batches_one_params(requests_mock, toloka_client_prod, toloka_app_url, app_batch_map):
    app_batches = [dict(app_batch_map, id=str(i)) for i in range(10)]
    app_batches.sort(key=itemgetter('id'))
    expected_app_batches = [app_batch for app_batch in app_batches]

    def get_app_batches(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_batches',
            'X-Low-Level-Method': 'find_app_batches',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        assert {'after_id': ['1'], 'sort': ['id']} == params
        return {'content': [app_batch for app_batch in app_batches], 'has_more': False}

    requests_mock.get(f'{toloka_app_url}/app-projects/123/batches', json=get_app_batches)

    # Expanded positional syntax
    result = toloka_client_prod.get_app_batches('123', after_id='1')
    assert expected_app_batches == client.unstructure(list(result))


def test_get_app_batch(requests_mock, toloka_client_prod, toloka_app_url, app_batch_map):

    def get_app_batch(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_app_batch',
            'X-Low-Level-Method': 'get_app_batch',
        }
        check_headers(request, expected_headers)

        return app_batch_map

    requests_mock.get(f'{toloka_app_url}/app-projects/21/batches/123', json=get_app_batch)
    assert app_batch_map == client.unstructure(toloka_client_prod.get_app_batch('21', '123'))


def test_create_app_batch(requests_mock, toloka_client_prod, toloka_app_url, app_item_map, app_batch_map):

    app_batch_create_request = {
        'items': [app_item_map['input_data']]
    }

    def app_batch(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_app_batch',
            'X-Low-Level-Method': 'create_app_batch',
        }
        check_headers(request, expected_headers)

        assert app_batch_create_request == request.json()
        return app_batch_map

    requests_mock.post(f'{toloka_app_url}/app-projects/123/batches', json=app_batch, status_code=201)
    app_batch_create_request_obj = client.structure(app_batch_create_request, client.app.AppBatchCreateRequest)
    result = toloka_client_prod.create_app_batch('123', app_batch_create_request_obj)
    assert app_batch_map == client.unstructure(result)


def test_start_app_batch(requests_mock, toloka_client_prod, toloka_app_url):

    def start_app_batch(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'start_app_batch',
            'X-Low-Level-Method': 'start_app_batch',
        }
        check_headers(request, expected_headers)

    requests_mock.post(f'{toloka_app_url}/app-projects/123/batches/321/start', text=start_app_batch, status_code=201)
    toloka_client_prod.start_app_batch('123', '321')
