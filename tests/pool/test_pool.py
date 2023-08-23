import datetime
import logging
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import httpx
import pytest
import simplejson
import simplejson as json
import toloka.client as client
from httpx import QueryParams
from toloka.client.pool import Pool

from ..testutils.util_functions import check_headers


def test_find_pools(respx_mock, toloka_client, toloka_url, pool_map_with_readonly):
    raw_result = {'items': [pool_map_with_readonly], 'has_more': False}

    def pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_pools',
            'X-Low-Level-Method': 'find_pools',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            project_id='10',
            id_gt='20',
            last_started_lt='2016-03-23T12:59:00',
            sort='created,-id',
        ) == request.url.params
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.get(f'{toloka_url}/pools').mock(side_effect=pools)

    # Request object syntax
    request = client.search_requests.PoolSearchRequest(
        project_id='10',
        id_gt='20',
        last_started_lt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc),
    )
    sort = client.search_requests.PoolSortItems(['created', '-id'])
    result = toloka_client.find_pools(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_pools(
        project_id='10',
        id_gt='20',
        last_started_lt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc),
        sort=['created', '-id'],
    )
    assert raw_result == client.unstructure(result)


def test_get_pools(respx_mock, toloka_client, toloka_url, pool_map_with_readonly):
    pools = [dict(pool_map_with_readonly, id=str(i)) for i in range(100)]
    pools.sort(key=itemgetter('id'))
    expected_pools = [pool for pool in pools if pool['id'] > '20']

    def get_pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_pools',
            'X-Low-Level-Method': 'find_pools',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params['id_gt']
        params = params.remove('id_gt')
        assert QueryParams(
            project_id='10',
            last_started_lt='2016-03-23T12:59:00',
            sort='id',
        ) == params

        items = [pool for pool in pools if id_gt is None or pool['id'] > id_gt][:3]
        return httpx.Response(json={'items': items, 'has_more': items[-1]['id'] != pools[-1]['id']}, status_code=200)

    respx_mock.get(f'{toloka_url}/pools').mock(side_effect=get_pools)

    # Request object syntax
    request = client.search_requests.PoolSearchRequest(
        project_id='10',
        id_gt='20',
        last_started_lt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc),
    )
    result = toloka_client.get_pools(request)
    assert expected_pools == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_pools(
        project_id='10',
        id_gt='20',
        last_started_lt=datetime.datetime(2016, 3, 23, 12, 59, 0, tzinfo=datetime.timezone.utc),
    )
    assert expected_pools == client.unstructure(list(result))


def test_get_pools_one_params(respx_mock, toloka_client, toloka_url, pool_map_with_readonly):
    pools = [dict(pool_map_with_readonly, id=str(i)) for i in range(10)]
    pools.sort(key=itemgetter('id'))
    expected_pools = [pool for pool in pools]

    def get_pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_pools',
            'X-Low-Level-Method': 'find_pools',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        assert QueryParams(status='OPEN', sort='id') == params
        return httpx.Response(json={'items': [pool for pool in pools], 'has_more': False}, status_code=200)

    respx_mock.get(f'{toloka_url}/pools').mock(side_effect=get_pools)

    # Expanded positional syntax
    result = toloka_client.get_pools('OPEN')
    assert expected_pools == client.unstructure(list(result))


def test_get_pool(respx_mock, toloka_client, toloka_url, pool_map_with_readonly):

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=pool_map_with_readonly, status_code=200)

    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=pool)
    assert pool_map_with_readonly == client.unstructure(toloka_client.get_pool('21'))


def test_get_pool_training(respx_mock, toloka_client, toloka_url, training_pool_map):

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=training_pool_map, status_code=200)

    respx_mock.get(f'{toloka_url}/pools/22').mock(side_effect=pool)
    assert training_pool_map == client.unstructure(toloka_client.get_pool('22'))


def test_create_pool(respx_mock, toloka_client, toloka_url, pool_map, pool_map_with_readonly, caplog):

    def pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_pool',
            'X-Low-Level-Method': 'create_pool',
        }
        check_headers(request, expected_headers)

        assert pool_map == simplejson.loads(request.content)
        return httpx.Response(json=pool_map_with_readonly, status_code=201)

    respx_mock.post(f'{toloka_url}/pools').mock(side_effect=pools)
    pool = client.structure(pool_map, client.pool.Pool)
    with caplog.at_level(logging.INFO):
        caplog.clear()
        result = toloka_client.create_pool(pool)
        assert [log for log in caplog.record_tuples if log[0] == 'toloka.client'] == [(
            'toloka.client', logging.INFO,
            'A new pool with ID "21" has been created. Link to open in web interface: https://sandbox.toloka.yandex.com/requester/project/10/pool/21'
        )]
        assert pool_map_with_readonly == client.unstructure(result)


def test_create_pool_check_all_filters(respx_mock, toloka_client, toloka_url, pool_map_with_readonly):

    pool_map = {
        **pool_map_with_readonly,
        'filter': {
            'and': [
                {
                    'or': [
                        {'category': 'profile', 'key': 'gender', 'operator': 'EQ', 'value': 'FEMALE'},
                        {'category': 'profile', 'key': 'country', 'operator': 'NE', 'value': 'BE'},
                    ],
                },
                {'or': [{'category': 'profile', 'key': 'citizenship', 'operator': 'EQ', 'value': 'BY'}]},
                {'or': [{'category': 'profile', 'key': 'education', 'operator': 'EQ', 'value': 'MIDDLE'}]},
                {'or': [{'category': 'profile', 'key': 'adult_allowed', 'operator': 'EQ', 'value': True}]},
                {'or': [{'category': 'profile', 'key': 'date_of_birth', 'operator': 'GT', 'value': 604972800}]},
                {'or': [{'category': 'profile', 'key': 'city', 'operator': 'NOT_IN', 'value': 225}]},
                {'or': [{'category': 'profile', 'key': 'languages', 'operator': 'IN', 'value': 'RU'}]},
                {'or': [{'category': 'profile', 'key': 'verified', 'operator': 'EQ', 'value': True}]},
                {
                    'and': [
                        {'category': 'computed', 'key': 'region_by_phone', 'operator': 'IN', 'value': 213},
                        {'category': 'computed', 'key': 'region_by_ip', 'operator': 'NOT_IN', 'value': 1},
                    ]
                },
                {'or': [{'category': 'computed', 'key': 'device_category', 'operator': 'EQ', 'value': 'PERSONAL_COMPUTER'}]},
                {'or': [{'category': 'computed', 'key': 'os_family', 'operator': 'EQ', 'value': 'WINDOWS'}]},
                {'or': [{'category': 'computed', 'key': 'os_version', 'operator': 'GTE', 'value': 8.1}]},
                {'or': [{'category': 'computed', 'key': 'os_version_major', 'operator': 'GT', 'value': 8}]},
                {'or': [{'category': 'computed', 'key': 'os_version_minor', 'operator': 'GTE', 'value': 1}]},
                {'or': [{'category': 'computed', 'key': 'os_version_bugfix', 'operator': 'LTE', 'value': 225}]},
                {'or': [{'category': 'computed', 'key': 'user_agent_type', 'operator': 'EQ', 'value': 'BROWSER'}]},
                # {'category': 'computed', 'key': 'user_agent_family', 'operator': 'NE', 'value': 'OPERA'},
                {'or': [{'category': 'computed', 'key': 'user_agent_version', 'operator': 'LT', 'value': 11.12}]},
                {'or': [{'category': 'computed', 'key': 'user_agent_version_major', 'operator': 'LT', 'value': 11}]},
                {'or': [{'category': 'computed', 'key': 'user_agent_version_minor', 'operator': 'LT', 'value': 12}]},
                {'or': [{'category': 'computed', 'key': 'user_agent_version_bugfix', 'operator': 'GT', 'value': 2026}]},
                {
                    'or': [
                        {'category': 'skill', 'key': '224', 'operator': 'GTE', 'value': 85},
                        {'category': 'skill', 'key': '300', 'operator': 'NE', 'value': None},
                        {'category': 'skill', 'key': '350', 'operator': 'EQ', 'value': 75.512},
                    ]
                }
            ]
        }
    }

    def pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_pool',
            'X-Low-Level-Method': 'create_pool',
        }
        check_headers(request, expected_headers)

        assert pool_map == simplejson.loads(request.content)
        return httpx.Response(json=pool_map, status_code=201)

    respx_mock.post(f'{toloka_url}/pools').mock(side_effect=pools)

    import toloka.client.filter as filter

    pool = client.structure(pool_map_with_readonly, client.pool.Pool)
    pool.filter = (
        ((filter.Gender == filter.Gender.FEMALE) | (filter.Country != 'BE')) &
        (filter.Citizenship == 'BY') &
        (filter.Education == filter.Education.MIDDLE) &
        (filter.AdultAllowed == True) &  # noqa: E712
        (filter.DateOfBirth > 604972800) &
        (filter.City.not_in(225)) &
        (filter.Languages.in_('RU')) &
        (filter.Verified == True) &  # noqa: E712
        (filter.RegionByPhone.in_(213) & filter.RegionByIp.not_in(1)) &
        (filter.DeviceCategory == filter.DeviceCategory.PERSONAL_COMPUTER) &
        (filter.OSFamily == filter.OSFamily.WINDOWS) &
        (filter.OSVersion >= 8.1) &
        (filter.OSVersionMajor > 8) &
        (filter.OSVersionMinor >= 1) &
        (filter.OSVersionBugfix <= 225) &
        (filter.UserAgentType == filter.UserAgentType.BROWSER) &
        (filter.UserAgentVersion < 11.12) &
        (filter.UserAgentVersionMajor < 11) &
        (filter.UserAgentVersionMinor < 12) &
        (filter.UserAgentVersionBugfix > 2026) &
        ((filter.Skill('224') >= 85) | (filter.Skill('300') != None) | (filter.Skill('350') == 75.512))  # noqa: E711
    )
    result = toloka_client.create_pool(pool)
    assert client.structure(pool_map, client.pool.Pool) == result
    assert pool_map == client.unstructure(result)


@pytest.mark.parametrize('expire_time', [
    datetime.datetime.now(),
    datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=10))),
    datetime.datetime.now(tz=datetime.timezone.utc),
])
def test_create_pool_time_format(expire_time):
    pool = Pool(will_expire=expire_time)
    pool = Pool.structure(pool.unstructure())
    assert pool.will_expire.tzinfo == datetime.timezone.utc
    if expire_time.tzinfo is None:
        expire_time = expire_time.replace(tzinfo=datetime.timezone.utc)
    assert expire_time.astimezone(datetime.timezone.utc) == pool.will_expire


@pytest.mark.parametrize('tier', ['eu', None])
def test_create_pool_with_tier(respx_mock, toloka_client, toloka_url, pool_map, pool_map_with_readonly, caplog, tier):

    def pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_pool',
            'X-Low-Level-Method': 'create_pool',
        }
        check_headers(request, expected_headers)

        assert request.url.params == (QueryParams(storage_key=tier) if tier is not None else QueryParams())
        assert pool_map == simplejson.loads(request.content)
        return httpx.Response(json=pool_map_with_readonly, status_code=201)

    respx_mock.post(f'{toloka_url}/pools').mock(side_effect=pools)
    pool = client.structure(pool_map, client.pool.Pool)
    result = toloka_client.create_pool(pool, tier=tier)
    assert pool_map_with_readonly == client.unstructure(result)


@pytest.fixture
def pool_map_without_filter(pool_map_with_readonly):
    pool_map_without_filter = pool_map_with_readonly.copy()
    del pool_map_without_filter['filter']
    return pool_map_without_filter


def test_unstructure_pool_check_one_filter_wrap(respx_mock, toloka_client, toloka_url, pool_map_without_filter):
    pool_map = {
        **pool_map_without_filter,
        'filter': {
            'and': [
                {'or': [{'category': 'profile', 'key': 'languages', 'operator': 'IN', 'value': 'EN'}]},
            ]
        }
    }

    def pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_pool',
            'X-Low-Level-Method': 'create_pool',
        }
        check_headers(request, expected_headers)

        assert pool_map == simplejson.loads(request.content)
        return httpx.Response(json=pool_map, status_code=201)

    respx_mock.post(f'{toloka_url}/pools').mock(side_effect=pools)

    import toloka.client.filter as filter

    pool = client.structure(pool_map_without_filter, client.pool.Pool)
    pool.filter = filter.Languages.in_('EN')
    result = toloka_client.create_pool(pool)
    assert client.structure(pool_map, client.pool.Pool) == result
    assert pool_map == client.unstructure(result)


def test_unstructure_pool_filter_after_init():
    import toloka.client.filter as filter

    pool = client.pool.Pool(
        project_id=42,
        private_name='Pool 1',
        may_contain_adult_content=False,
        reward_per_assignment=1000.01,
        assignment_max_duration_seconds=10,
        defaults=client.pool.Pool.Defaults(default_overlap_for_new_task_suites=1),
        # we testing just this:
        filter=filter.Languages.in_('EN')
    )

    filter_map = {
        'and': [
            {'or': [{'category': 'profile', 'key': 'languages', 'operator': 'IN', 'value': 'EN'}]},
        ]
    }

    unstructed_pool = client.unstructure(pool)
    assert 'filter' in unstructed_pool
    assert filter_map == unstructed_pool['filter']


def test_pool_from_json(pool_map):
    pool = client.structure(pool_map, client.pool.Pool)
    pool_json = json.dumps(pool_map, use_decimal=True, ensure_ascii=False)
    pool_from_json = client.pool.Pool.from_json(pool_json)
    assert pool == pool_from_json


def test_pool_to_json(pool_map):
    pool = client.structure(pool_map, client.pool.Pool)
    pool_json = pool.to_json()
    pool_json_basic = json.dumps(pool_map, use_decimal=True, ensure_ascii=False)
    assert json.loads(pool_json) == json.loads(pool_json_basic)


def test_update_pool(respx_mock, toloka_client, toloka_url, pool_map_with_readonly):
    updated_pool = {
        **pool_map_with_readonly,
        'private_name': 'updated name',
        'private_comment': 'updated comment',
    }

    def pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'update_pool',
            'X-Low-Level-Method': 'update_pool',
        }
        check_headers(request, expected_headers)

        assert updated_pool == simplejson.loads(request.content)
        return httpx.Response(json=updated_pool, status_code=200)

    respx_mock.put(f'{toloka_url}/pools/21').mock(side_effect=pools)
    result = toloka_client.update_pool('21', client.structure(updated_pool, client.pool.Pool))
    assert updated_pool == client.unstructure(result)


def test_patch_pool(respx_mock, toloka_client, toloka_url, pool_map_with_readonly):
    raw_result = {**pool_map_with_readonly, 'priority': 42}

    def pools(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_pool',
            'X-Low-Level-Method': 'patch_pool',
        }
        check_headers(request, expected_headers)

        assert {'priority': 42} == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/pools/21').mock(side_effect=pools)

    # Request object syntax
    result = toloka_client.patch_pool('21', client.pool.PoolPatchRequest(priority=42))
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_pool('21', priority=42)
    assert raw_result == client.unstructure(result)

    # Expanded positional syntax
    result = toloka_client.patch_pool('21', 42)
    assert raw_result == client.unstructure(result)


@pytest.fixture
def open_pool_operation_map():
    return {
        'id': 'open-pool-op1id',
        'type': 'POOL.OPEN',
        'status': 'RUNNING',
        'submitted': '2016-03-07T15:47:00',
        'started': '2016-03-07T15:47:21',
        'parameters': {'pool_id': '21'},
    }


@pytest.fixture
def complete_open_pool_operation_map(open_pool_operation_map):
    return {
        **open_pool_operation_map,
        'status': 'SUCCESS',
        'finished': '2016-03-07T15:48:03',
    }


def test_open_pool_async(respx_mock, toloka_client, toloka_url, open_pool_operation_map, complete_open_pool_operation_map):

    def open_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'open_pool_async',
            'X-Low-Level-Method': 'open_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=open_pool_operation_map, status_code=202)

    def complete_open_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'wait_operation',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_open_pool_operation_map, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/open').mock(side_effect=open_pool)
    respx_mock.get(f'{toloka_url}/operations/{open_pool_operation_map["id"]}').mock(side_effect=complete_open_pool)

    operation = toloka_client.open_pool_async('21')
    assert open_pool_operation_map == client.unstructure(operation)

    complete_operation = toloka_client.wait_operation(operation)
    assert complete_open_pool_operation_map == client.unstructure(complete_operation)


def test_open_pool(respx_mock, toloka_client, toloka_url,
                   open_pool_operation_map, complete_open_pool_operation_map, open_pool_map_with_readonly):

    def open_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'open_pool',
            'X-Low-Level-Method': 'open_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=open_pool_operation_map, status_code=202)

    def complete_open_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'open_pool',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_open_pool_operation_map, status_code=200)

    def get_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'open_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=open_pool_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/open').mock(side_effect=open_pool)
    respx_mock.get(f'{toloka_url}/operations/{open_pool_operation_map["id"]}').mock(side_effect=complete_open_pool)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=get_pool)

    result = toloka_client.open_pool('21')
    assert open_pool_map_with_readonly == client.unstructure(result)


def test_open_pool_opened(respx_mock, toloka_client, toloka_url, open_pool_map_with_readonly):

    def get_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'open_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=open_pool_map_with_readonly, status_code=204)

    respx_mock.post(f'{toloka_url}/pools/21/open').respond(status_code=204)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=get_pool)
    result = toloka_client.open_pool('21')
    assert open_pool_map_with_readonly == client.unstructure(result)


@pytest.fixture
def empty_pool_error():
    return {
        'request_id': '8dff48b8e99cd9408fa2d6a906d52205',
        'code': 'EMPTY_POOL',
        'message': 'Pool contains no tasks. Operation is not allowed',
        'payload': None,
    }


def test_open_pool_exception(respx_mock, toloka_client, toloka_url, empty_pool_error):

    def get_empty_pool_error(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'open_pool',
            'X-Low-Level-Method': 'open_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=empty_pool_error, status_code=409)

    respx_mock.post(f'{toloka_url}/pools/21/open').mock(side_effect=get_empty_pool_error)
    with pytest.raises(client.exceptions.IncorrectActionsApiError):
        toloka_client.open_pool('21')


def test_open_pool_already_open(respx_mock, toloka_client, toloka_url, open_pool_map_with_readonly):

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'open_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)
        return httpx.Response(json=open_pool_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/open').respond(status_code=204)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=pool)
    assert toloka_client.open_pool_async('21') is None
    result = toloka_client.open_pool('21')
    assert open_pool_map_with_readonly == client.unstructure(result)


@pytest.fixture
def close_pool_operation_map():
    return {
        'id': 'close-pool-op1id',
        'type': 'POOL.CLOSE',
        'status': 'RUNNING',
        'submitted': '2016-07-22T13:04:00',
        'started': '2016-07-22T13:04:01',
        'finished': '2016-07-22T13:04:02',
        'parameters': {'pool_id': '21'},
    }


@pytest.fixture
def complete_close_pool_operation_map(close_pool_operation_map):
    return {
        **close_pool_operation_map,
        'status': 'SUCCESS',
    }


def test_close_pool_async(respx_mock, toloka_client, toloka_url, complete_close_pool_operation_map):

    def complete_close_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool_async',
            'X-Low-Level-Method': 'close_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_close_pool_operation_map, status_code=202)

    def async_operation(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'wait_operation',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)
        return httpx.Response(status_code=202)

    respx_mock.post(f'{toloka_url}/pools/21/close').mock(side_effect=complete_close_pool)
    op = toloka_client.close_pool_async('21')
    respx_mock.get(f'{toloka_url}/operations/{op.id}').mock(side_effect=async_operation)
    result = toloka_client.wait_operation(op)
    assert complete_close_pool_operation_map == client.unstructure(result)


def test_close_pool(respx_mock, toloka_client, toloka_url,
                    close_pool_operation_map, complete_close_pool_operation_map, pool_map_with_readonly):

    def close_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool',
            'X-Low-Level-Method': 'close_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=close_pool_operation_map, status_code=202)

    def complete_close_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_close_pool_operation_map, status_code=200)

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=pool_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/close').mock(side_effect=close_pool)
    respx_mock.get(f'{toloka_url}/operations/{close_pool_operation_map["id"]}').mock(side_effect=complete_close_pool)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=pool)

    result = toloka_client.close_pool('21')
    assert pool_map_with_readonly == client.unstructure(result)


def test_close_pool_already_closed(respx_mock, toloka_client, toloka_url, pool_map_with_readonly):

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=pool_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/close').respond(status_code=204)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=pool)
    assert toloka_client.close_pool_async('21') is None
    result = toloka_client.close_pool('21')
    assert pool_map_with_readonly == client.unstructure(result)


@pytest.fixture
def close_for_update_pool_operation_map():
    return {
        'id': 'close-pool-for-update-op1id',
        'type': 'POOL.CLOSE',
        'status': 'RUNNING',
        'submitted': '2016-07-22T13:04:00',
        'started': '2016-07-22T13:04:01',
        'finished': '2016-07-22T13:04:02',
        'parameters': {'pool_id': '21'},
    }


@pytest.fixture
def complete_close_for_update_pool_operation_map(close_for_update_pool_operation_map):
    return {
        **close_for_update_pool_operation_map,
        'status': 'SUCCESS',
    }


def test_close_pool_for_update_async(respx_mock, toloka_client, toloka_url,
                                     complete_close_for_update_pool_operation_map):

    def complete_close_for_update_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool_for_update_async',
            'X-Low-Level-Method': 'close_pool_for_update_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_close_for_update_pool_operation_map, status_code=202)

    respx_mock.post(f'{toloka_url}/pools/21/close-for-update').mock(side_effect=complete_close_for_update_pool)
    result = toloka_client.wait_operation(toloka_client.close_pool_for_update_async('21'))
    assert complete_close_for_update_pool_operation_map == client.unstructure(result)


def test_close_pool_for_update(respx_mock, toloka_client, toloka_url,
                               close_for_update_pool_operation_map, complete_close_for_update_pool_operation_map,
                               pool_map_with_readonly):

    def close_for_update_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool_for_update',
            'X-Low-Level-Method': 'close_pool_for_update_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=close_for_update_pool_operation_map, status_code=202)

    def complete_close_for_update_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool_for_update',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_close_for_update_pool_operation_map, status_code=200)

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool_for_update',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=pool_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/close-for-update').mock(side_effect=close_for_update_pool,)
    respx_mock.get(
        f'{toloka_url}/operations/{close_for_update_pool_operation_map["id"]}'
    ).mock(side_effect=complete_close_for_update_pool)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=pool)

    result = toloka_client.close_pool_for_update('21')
    assert pool_map_with_readonly == client.unstructure(result)


def test_close_pool_for_update_already_closed_for_update(respx_mock, toloka_client, toloka_url,
                                                         pool_map_with_readonly):

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'close_pool_for_update',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=pool_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/close-for-update').respond(204)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=pool)
    assert toloka_client.close_pool_for_update_async('21') is None
    result = toloka_client.close_pool_for_update('21')
    assert pool_map_with_readonly == client.unstructure(result)


@pytest.fixture
def archive_pool_operation_map():
    return {
        'id': 'archive-pool-op1id',
        'type': 'POOL.ARCHIVE',
        'status': 'RUNNING',
        'submitted': '2016-07-22T13:04:00',
        'started': '2016-07-22T13:04:01',
        'finished': '2016-07-22T13:04:02',
        'parameters': {'pool_id': '21'},
    }


@pytest.fixture
def complete_archive_pool_operation_map(archive_pool_operation_map):
    return {
        **archive_pool_operation_map,
        'status': 'SUCCESS',
    }


def test_archive_pool_async(respx_mock, toloka_client, toloka_url, complete_archive_pool_operation_map):

    def complete_archive_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'archive_pool_async',
            'X-Low-Level-Method': 'archive_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_archive_pool_operation_map, status_code=202)

    respx_mock.post(f'{toloka_url}/pools/21/archive').mock(side_effect=complete_archive_pool)
    result = toloka_client.wait_operation(toloka_client.archive_pool_async('21'))
    assert complete_archive_pool_operation_map == client.unstructure(result)


def test_archive_pool(respx_mock, toloka_client, toloka_url,
                      archive_pool_operation_map, complete_archive_pool_operation_map, pool_map_with_readonly):

    def archive_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'archive_pool',
            'X-Low-Level-Method': 'archive_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=archive_pool_operation_map, status_code=202)

    def complete_archive_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'archive_pool',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_archive_pool_operation_map, status_code=200)

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'archive_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=pool_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/archive').mock(side_effect=archive_pool)
    respx_mock.get(
        f'{toloka_url}/operations/{archive_pool_operation_map["id"]}'
    ).mock(side_effect=complete_archive_pool)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=pool)

    result = toloka_client.archive_pool('21')
    assert pool_map_with_readonly == client.unstructure(result)


def test_archive_pool_already_archived(respx_mock, toloka_client, toloka_url, archived_pool_map_with_readonly):

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'archive_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=archived_pool_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/archive').respond(status_code=204)
    respx_mock.get(f'{toloka_url}/pools/21').mock(side_effect=pool)
    assert toloka_client.archive_pool_async('21') is None
    result = toloka_client.archive_pool('21')
    assert archived_pool_map_with_readonly == client.unstructure(result)


@pytest.fixture
def clone_pool_operation_map():
    return {
        'id': 'archive-pool-op1id',
        'type': 'POOL.CLONE',
        'status': 'RUNNING',
        'submitted': '2016-07-22T13:04:00',
        'started': '2016-07-22T13:04:01',
        'finished': '2016-07-22T13:04:02',
        'parameters': {'pool_id': '21'},
    }


@pytest.fixture
def complete_clone_pool_operation_map(clone_pool_operation_map):
    return {
        **clone_pool_operation_map,
        'status': 'SUCCESS',
        'details': {'pool_id': '22'},
    }


@pytest.fixture
def cloned_pool_map(pool_map_with_readonly):
    return {
        **pool_map_with_readonly,
        'id': '22',
    }


def test_clone_pool_async(respx_mock, toloka_client, toloka_url, complete_clone_pool_operation_map):

    def complete_clone_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_pool_async',
            'X-Low-Level-Method': 'clone_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_clone_pool_operation_map, status_code=202)

    respx_mock.post(f'{toloka_url}/pools/21/clone').mock(side_effect=complete_clone_pool)
    result = toloka_client.wait_operation(toloka_client.clone_pool_async('21'))
    assert complete_clone_pool_operation_map == client.unstructure(result)


def test_clone_pool(respx_mock, toloka_client, toloka_url,
                    clone_pool_operation_map, complete_clone_pool_operation_map, cloned_pool_map, caplog):

    def clone_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_pool',
            'X-Low-Level-Method': 'clone_pool_async',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=clone_pool_operation_map, status_code=202)

    def complete_clone_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_pool',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=complete_clone_pool_operation_map, status_code=200)

    def pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_pool',
            'X-Low-Level-Method': 'get_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=cloned_pool_map, status_code=200)

    respx_mock.post(f'{toloka_url}/pools/21/clone').mock(side_effect=clone_pool)
    respx_mock.get(f'{toloka_url}/operations/{clone_pool_operation_map["id"]}').mock(side_effect=complete_clone_pool)
    respx_mock.get(f'{toloka_url}/pools/22').mock(side_effect=pool)

    with caplog.at_level(logging.INFO):
        caplog.clear()
        result = toloka_client.clone_pool('21')
        assert [log for log in caplog.record_tuples if log[0] == 'toloka.client'] == [(
            'toloka.client',
            logging.INFO,
            'A new pool with ID "22" has been cloned. Link to open in web interface: https://sandbox.toloka.yandex.com/requester/project/10/pool/22'
        )]
        assert cloned_pool_map == client.unstructure(result)


@pytest.fixture
def simple_project_with_mixer_config():
    return {
        'project_id': '12345',
        'defaults': {'default_overlap_for_new_task_suites': 1},
        'quality_control': {'configs': []},
        'mixer_config': {'real_tasks_count': 1, 'golden_tasks_count': 0, 'training_tasks_count': 0},
    }


def test_mixer_config_expand(simple_project_with_mixer_config):
    pool = client.Pool(project_id='12345')
    pool.set_mixer_config(real_tasks_count=1)
    assert client.unstructure(pool) == simple_project_with_mixer_config

    with pytest.raises(TypeError):
        pool.set_mixer_config(1)
