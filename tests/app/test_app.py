import copy
import datetime
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams
from toloka.client.app import AppItemCreateRequest, SyncBatchCreateRequest

from ..testutils.util_functions import check_headers


def test_find_apps(respx_mock, toloka_client_prod, toloka_app_url, app_map):
    raw_result = {'content': [app_map], 'has_more': False}

    def apps(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_apps',
            'X-Low-Level-Method': 'find_apps',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            after_id='123', lang='en', sort='-id'
        ) == request.url.params
        return httpx.Response(text=simplejson.dumps(raw_result), status_code=200)

    respx_mock.get(f'{toloka_app_url}/apps').mock(side_effect=apps)

    # Request object syntax
    request = client.search_requests.AppSearchRequest(
        after_id='123', lang='en'
    )
    sort = client.search_requests.AppSortItems(['-id'])
    result = toloka_client_prod.find_apps(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client_prod.find_apps(
        after_id='123', lang='en',
        sort=['-id'],
    )
    assert raw_result == client.unstructure(result)


def test_get_apps(respx_mock, toloka_client_prod, toloka_app_url, app_map):
    apps = [dict(app_map, id=str(i)) for i in range(100)]
    apps.sort(key=itemgetter('id'))
    expected_apps = [app for app in apps if app['id'] > '20']

    def get_apps(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_apps',
            'X-Low-Level-Method': 'find_apps',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params['id_gt']
        params = params.remove('id_gt')
        assert QueryParams(
            sort='id',
        ) == params

        items = [app for app in apps if id_gt is None or app['id'] > id_gt][:3]
        return httpx.Response(
            text=simplejson.dumps({'content': items, 'has_more': items[-1]['id'] != apps[-1]['id']}), status_code=200
        )

    respx_mock.get(f'{toloka_app_url}/apps').mock(side_effect=get_apps)

    # Request object syntax
    request = client.search_requests.AppSearchRequest(
        id_gt='20',
    )
    result = toloka_client_prod.get_apps(request)
    assert expected_apps == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client_prod.get_apps(
        id_gt='20',
    )
    assert expected_apps == client.unstructure(list(result))


def test_get_apps_one_params(respx_mock, toloka_client_prod, toloka_app_url, app_map):
    apps = [dict(app_map, id=str(i)) for i in range(10)]
    apps.sort(key=itemgetter('id'))
    expected_apps = [app for app in apps]

    def get_apps(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_apps',
            'X-Low-Level-Method': 'find_apps',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        assert QueryParams(after_id='1', sort='id') == params
        return httpx.Response(
            text=simplejson.dumps({'content': [app for app in apps], 'has_more': False}), status_code=200
        )

    respx_mock.get(f'{toloka_app_url}/apps').mock(side_effect=get_apps)

    # Expanded positional syntax
    result = toloka_client_prod.get_apps(after_id='1')
    assert expected_apps == client.unstructure(list(result))


def test_get_app(respx_mock, toloka_client_prod, toloka_app_url, app_map):

    def get_app(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app',
            'X-Low-Level-Method': 'get_app',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(app_map), status_code=200)

    respx_mock.get(f'{toloka_app_url}/apps/21').mock(side_effect=get_app)
    assert app_map == client.unstructure(toloka_client_prod.get_app('21', 'en'))


def test_find_app_projects(respx_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):
    raw_result = {'content': [app_project_map_with_readonly], 'has_more': False}

    def app_projects(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_app_projects',
            'X-Low-Level-Method': 'find_app_projects',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            app_id='123',
            sort='name,-id',
        ) == request.url.params
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.get(f'{toloka_app_url}/app-projects').mock(side_effect=app_projects)

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


def test_get_app_projects(respx_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):
    app_projects = [dict(app_project_map_with_readonly, id=str(i)) for i in range(100)]
    app_projects.sort(key=itemgetter('id'))
    expected_app_projects = [project for project in app_projects if project['id'] > '20']

    def get_app_projects(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_projects',
            'X-Low-Level-Method': 'find_app_projects',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params['id_gt']
        params = params.remove('id_gt')
        assert QueryParams(
            sort='id',
            created_gt='2016-03-23T12:59:00'
        ) == params

        items = [project for project in app_projects if id_gt is None or project['id'] > id_gt][:3]
        return httpx.Response(
            json={'content': items, 'has_more': items[-1]['id'] != app_projects[-1]['id']}, status_code=200
        )

    respx_mock.get(f'{toloka_app_url}/app-projects').mock(side_effect=get_app_projects)

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


def test_get_app_projects_one_params(respx_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):
    app_projects = [dict(app_project_map_with_readonly, id=str(i)) for i in range(10)]
    app_projects.sort(key=itemgetter('id'))
    expected_app_projects = [project for project in app_projects]

    def get_app_projects(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_projects',
            'X-Low-Level-Method': 'find_app_projects',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        assert QueryParams(status='READY', sort='id') == params
        return httpx.Response(
            json={'content': [project for project in app_projects], 'has_more': False}, status_code=200
        )

    respx_mock.get(f'{toloka_app_url}/app-projects').mock(side_effect=get_app_projects)

    # Expanded positional syntax
    result = toloka_client_prod.get_app_projects(status='READY')
    assert expected_app_projects == client.unstructure(list(result))


def test_get_app_project(respx_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):

    def get_app_project(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_project',
            'X-Low-Level-Method': 'get_app_project',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=app_project_map_with_readonly, status_code=200)

    respx_mock.get(f'{toloka_app_url}/app-projects/123').mock(side_effect=get_app_project)
    assert app_project_map_with_readonly == client.unstructure(toloka_client_prod.get_app_project('123'))


def test_create_app_project(respx_mock, toloka_client_prod, toloka_app_url, app_map, app_project_map_with_readonly):

    def app_projects(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_app_project',
            'X-Low-Level-Method': 'create_app_project',
        }
        check_headers(request, expected_headers)

        assert app_map == simplejson.loads(request.content)
        return httpx.Response(json=app_project_map_with_readonly, status_code=201)

    respx_mock.post(f'{toloka_app_url}/app-projects').mock(side_effect=app_projects)
    app_project = client.structure(app_map, client.app.App)
    result = toloka_client_prod.create_app_project(app_project)
    assert app_project_map_with_readonly == client.unstructure(result)


def test_archive_app_project(respx_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):

    def archive_app_project(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'archive_app_project',
            'X-Low-Level-Method': 'archive_app_project',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=app_project_map_with_readonly, status_code=200)

    def get_app_project(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'archive_app_project',
            'X-Low-Level-Method': 'get_app_project',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=app_project_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_app_url}/app-projects/123/archive').mock(side_effect=archive_app_project)
    respx_mock.get(f'{toloka_app_url}/app-projects/123').mock(side_effect=get_app_project)
    assert app_project_map_with_readonly == client.unstructure(toloka_client_prod.archive_app_project('123'))


def test_unarchive_app_project(respx_mock, toloka_client_prod, toloka_app_url, app_project_map_with_readonly):

    def unarchive_app_project(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'unarchive_app_project',
            'X-Low-Level-Method': 'unarchive_app_project',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=app_project_map_with_readonly, status_code=200)

    def get_app_project(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'unarchive_app_project',
            'X-Low-Level-Method': 'get_app_project',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=app_project_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_app_url}/app-projects/123/unarchive').mock(side_effect=unarchive_app_project)
    respx_mock.get(f'{toloka_app_url}/app-projects/123').mock(side_effect=get_app_project)
    assert app_project_map_with_readonly == client.unstructure(toloka_client_prod.unarchive_app_project('123'))


def test_find_app_items(respx_mock, toloka_client_prod, toloka_app_url, app_item_map_with_readonly):
    raw_result = {'content': [app_item_map_with_readonly], 'has_more': False}

    def app_items(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_app_items',
            'X-Low-Level-Method': 'find_app_items',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            after_id='123',
            sort='created,-id,finished',
        ) == request.url.params
        return httpx.Response(text=simplejson.dumps(raw_result), status_code=200)

    respx_mock.get(f'{toloka_app_url}/app-projects/123/items').mock(side_effect=app_items)

    # Request object syntax
    request = client.search_requests.AppItemSearchRequest(
        after_id='123',
    )
    sort = client.search_requests.AppItemSortItems(['created', '-id', 'finished'])
    result = toloka_client_prod.find_app_items('123', request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client_prod.find_app_items(
        '123',
        after_id='123',
        sort=['created', '-id', 'finished'],
    )
    assert raw_result == client.unstructure(result)


def test_get_app_items(respx_mock, toloka_client_prod, toloka_app_url, app_item_map_with_readonly):
    app_items = [dict(app_item_map_with_readonly, id=str(i)) for i in range(100)]
    app_items.sort(key=itemgetter('id'))
    expected_app_items = [app_item for app_item in app_items if app_item['id'] > '20']

    def get_app_items(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_items',
            'X-Low-Level-Method': 'find_app_items',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params['id_gt']
        params = params.remove('id_gt')
        assert QueryParams(
            sort='id',
            created_gt='2016-03-23T12:59:00',
        ) == params

        items = [app_item for app_item in app_items if id_gt is None or app_item['id'] > id_gt][:3]
        return httpx.Response(
            text=simplejson.dumps({'content': items, 'has_more': items[-1]['id'] != app_items[-1]['id']}),
            status_code=200
        )

    respx_mock.get(f'{toloka_app_url}/app-projects/123/items').mock(side_effect=get_app_items)

    # Request object syntax
    request = client.search_requests.AppItemSearchRequest(
        id_gt='20',
        created_gt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc)
    )
    result = toloka_client_prod.get_app_items('123', request)
    assert expected_app_items == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client_prod.get_app_items(
        '123',
        id_gt='20',
        created_gt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc)
    )
    assert expected_app_items == client.unstructure(list(result))


def test_get_app_items_one_params(respx_mock, toloka_client_prod, toloka_app_url, app_item_map_with_readonly):
    app_items = [dict(app_item_map_with_readonly, id=str(i)) for i in range(10)]
    app_items.sort(key=itemgetter('id'))
    expected_app_items = [app_item for app_item in app_items]

    def get_app_items(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_items',
            'X-Low-Level-Method': 'find_app_items',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        assert QueryParams(after_id='1', sort='id') == params
        return httpx.Response(
            text=simplejson.dumps({'content': [app_item for app_item in app_items], 'has_more': False}),
            status_code=200
        )

    respx_mock.get(f'{toloka_app_url}/app-projects/123/items').mock(side_effect=get_app_items)

    # Expanded positional syntax
    result = toloka_client_prod.get_app_items('123', after_id='1')
    assert expected_app_items == client.unstructure(list(result))


def test_get_app_item(respx_mock, toloka_client_prod, toloka_app_url, app_item_map_with_readonly):

    def get_app_item(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_item',
            'X-Low-Level-Method': 'get_app_item',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(app_item_map_with_readonly), status_code=200)

    respx_mock.get(f'{toloka_app_url}/app-projects/21/items/123').mock(side_effect=get_app_item)
    assert app_item_map_with_readonly == client.unstructure(toloka_client_prod.get_app_item('21', '123'))


def test_create_app_item(respx_mock, toloka_client_prod, toloka_app_url, app_item_map, app_item_map_with_readonly):

    def app_items(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_app_item',
            'X-Low-Level-Method': 'create_app_item',
        }
        check_headers(request, expected_headers)

        expected_request = AppItemCreateRequest(
            batch_id=app_item_map['batch_id'],
            input_data=app_item_map['input_data'],
            force_new_original=True,
        )
        assert expected_request.unstructure() == simplejson.loads(request.content)
        return httpx.Response(text=simplejson.dumps(app_item_map_with_readonly), status_code=201)

    respx_mock.post(f'{toloka_app_url}/app-projects/123/items').mock(side_effect=app_items)
    app_item = client.structure(app_item_map, client.app.AppItem)
    result = toloka_client_prod.create_app_item('123', app_item, force_new_original=True)
    assert app_item_map_with_readonly == client.unstructure(result)


def test_create_app_item_expanded(
    respx_mock, toloka_client_prod, toloka_app_url, app_item_map, app_item_map_with_readonly,
):
    def app_items(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_app_item',
            'X-Low-Level-Method': 'create_app_item',
        }
        check_headers(request, expected_headers)

        assert app_item_map == simplejson.loads(request.content)
        return httpx.Response(text=simplejson.dumps(app_item_map_with_readonly), status_code=201)

    respx_mock.post(f'{toloka_app_url}/app-projects/123/items').mock(side_effect=app_items)
    result = toloka_client_prod.create_app_item('123', **app_item_map)
    assert app_item_map_with_readonly == client.unstructure(result)


def test_create_app_items(respx_mock, toloka_client_prod, toloka_app_url, app_item_map, app_item_map_with_readonly):
    expected_app_item_ids = ['created-app-item-id']
    app_items_create_request = {
        'batch_id': app_item_map['batch_id'],
        'items': [app_item_map['input_data']]
    }

    def app_items(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_app_items',
            'X-Low-Level-Method': 'create_app_items',
        }
        check_headers(request, expected_headers)

        assert app_items_create_request == simplejson.loads(request.content)
        return httpx.Response(status_code=201, json=expected_app_item_ids)

    respx_mock.post(f'{toloka_app_url}/app-projects/123/items/bulk').mock(side_effect=app_items)
    app_item = client.structure(app_items_create_request, client.app.AppItemsCreateRequest)
    app_item_ids = toloka_client_prod.create_app_items('123', app_item)
    assert app_item_ids == app_item_ids


def test_find_app_batches(respx_mock, toloka_client_prod, toloka_app_url, app_batch_map):
    raw_result = {'content': [app_batch_map], 'has_more': False}

    def app_batches(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_app_batches',
            'X-Low-Level-Method': 'find_app_batches',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            after_id='123',
            sort='created,-id',
        ) == request.url.params
        return httpx.Response(text=simplejson.dumps(raw_result), status_code=200)

    respx_mock.get(f'{toloka_app_url}/app-projects/123/batches').mock(side_effect=app_batches)

    # Request object syntax
    request = client.search_requests.AppBatchSearchRequest(
        after_id='123',
    )
    sort = client.search_requests.AppBatchSortItems(['created', '-id'])
    result = toloka_client_prod.find_app_batches('123', request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client_prod.find_app_batches(
        '123',
        after_id='123',
        sort=['created', '-id'],
    )
    assert raw_result == client.unstructure(result)


def test_get_app_batches(respx_mock, toloka_client_prod, toloka_app_url, app_batch_map):
    app_batches = [dict(app_batch_map, id=str(i)) for i in range(100)]
    app_batches.sort(key=itemgetter('id'))
    expected_app_batches = [app_batch for app_batch in app_batches if app_batch['id'] > '20']

    def get_app_batches(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_batches',
            'X-Low-Level-Method': 'find_app_batches',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params['id_gt']
        params = params.remove('id_gt')
        assert QueryParams(
            sort='id',
            name_gt='name',
        ) == params

        items = [app_batch for app_batch in app_batches if id_gt is None or app_batch['id'] > id_gt][:3]
        return httpx.Response(
            text=simplejson.dumps({'content': items, 'has_more': items[-1]['id'] != app_batches[-1]['id']}),
            status_code=200
        )

    respx_mock.get(f'{toloka_app_url}/app-projects/123/batches').mock(side_effect=get_app_batches)

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


def test_get_app_batches_one_params(respx_mock, toloka_client_prod, toloka_app_url, app_batch_map):
    app_batches = [dict(app_batch_map, id=str(i)) for i in range(10)]
    app_batches.sort(key=itemgetter('id'))
    expected_app_batches = [app_batch for app_batch in app_batches]

    def get_app_batches(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_batches',
            'X-Low-Level-Method': 'find_app_batches',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        assert QueryParams(after_id='1', sort='id') == params
        return httpx.Response(
            text=simplejson.dumps({'content': [app_batch for app_batch in app_batches], 'has_more': False}),
            status_code=200
        )

    respx_mock.get(f'{toloka_app_url}/app-projects/123/batches').mock(side_effect=get_app_batches)

    # Expanded positional syntax
    result = toloka_client_prod.get_app_batches('123', after_id='1')
    assert expected_app_batches == client.unstructure(list(result))


def test_get_app_batch(respx_mock, toloka_client_prod, toloka_app_url, app_batch_map):

    def get_app_batch(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_app_batch',
            'X-Low-Level-Method': 'get_app_batch',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(app_batch_map), status_code=200)

    respx_mock.get(f'{toloka_app_url}/app-projects/21/batches/123').mock(side_effect=get_app_batch)
    assert app_batch_map == client.unstructure(toloka_client_prod.get_app_batch(app_project_id='21', batch_id='123'))


def test_create_app_batch(respx_mock, toloka_client_prod, toloka_app_url, app_item_map, app_batch_map):

    app_batch_create_request = {
        'items': [app_item_map['input_data']],
        'priority_order': app_batch_map['priority_order'],
        'force_new_original': True,
        'ignore_errors': False,
    }

    def app_batch(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_app_batch',
            'X-Low-Level-Method': 'create_app_batch',
        }
        check_headers(request, expected_headers)

        assert app_batch_create_request == simplejson.loads(request.content)
        return httpx.Response(text=simplejson.dumps(app_batch_map), status_code=201)

    respx_mock.post(f'{toloka_app_url}/app-projects/123/batches').mock(side_effect=app_batch)
    app_batch_create_request_obj = client.structure(app_batch_create_request, client.app.AppBatchCreateRequest)
    result = toloka_client_prod.create_app_batch('123', app_batch_create_request_obj)
    assert app_batch_map == client.unstructure(result)


def test_start_sync_batch_processing(respx_mock, toloka_client_prod, toloka_app_url, app_item_map, app_batch_map):

    app_batch_create_request = {
        'items': [app_item_map['input_data']],
        'name': 'name',
    }

    def app_batch(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'start_sync_batch_processing',
            'X-Low-Level-Method': 'start_sync_batch_processing',
        }
        check_headers(request, expected_headers)

        assert app_batch_create_request == simplejson.loads(request.content)
        return httpx.Response(text=simplejson.dumps(app_batch_map), status_code=201)

    respx_mock.post(f'{toloka_app_url}/app-projects/123/batches/sync').mock(side_effect=app_batch)
    sync_batch_create_request_obj = SyncBatchCreateRequest.structure(app_batch_create_request)
    result = toloka_client_prod.start_sync_batch_processing(app_project_id='123', request=sync_batch_create_request_obj)
    assert app_batch_map == client.unstructure(result)


def test_patch_app_batch(respx_mock, toloka_client_prod, toloka_app_url, app_batch_map):

    app_batch_patch_request = {
        'name': 'new_name'
    }
    app_batch_map_patched = copy.deepcopy(app_batch_map)
    app_batch_map_patched['name'] = 'new_name'

    def patch_app_batch(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_app_batch',
            'X-Low-Level-Method': 'patch_app_batch',
        }
        check_headers(request, expected_headers)

        assert app_batch_patch_request == simplejson.loads(request.content)
        app_batch_map_copy = copy.deepcopy(app_batch_map)
        app_batch_map_copy['name'] = 'new_name'
        return httpx.Response(text=simplejson.dumps(app_batch_map_copy), status_code=200)

    respx_mock.patch(f'{toloka_app_url}/app-projects/123/batches/123').mock(side_effect=patch_app_batch)
    assert toloka_client_prod.patch_app_batch(
        '123', app_batch_map['id'], name='new_name'
    ).unstructure() == app_batch_map_patched


@pytest.mark.parametrize(
    'method_name', ('start_app_batch', 'stop_app_batch', 'resume_app_batch', 'archive_app_batch', 'unarchive_app_batch')
)
def test_change_app_batch_status(respx_mock, toloka_client_prod, toloka_app_url, method_name):

    def change_status(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client_prod, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': method_name,
            'X-Low-Level-Method': method_name,
        }
        check_headers(request, expected_headers)
        return httpx.Response(status_code=201)

    respx_mock.post(
        f'{toloka_app_url}/app-projects/123/batches/321/{method_name.split("_")[0]}'
    ).mock(side_effect=change_status)
    getattr(toloka_client_prod, method_name)('123', '321')
