import datetime
from copy import deepcopy
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams

from .testutils.util_functions import check_headers


@pytest.fixture
def message_thread_base_map():
    return {
        'id': 'message-thread-1',
        'topic': {'EN': 'Message title'},
        'interlocutors_inlined': True,
        'meta': {
            'pool_id': '1',
            'project_id': '2',
            'assignment_id': '3',
        },
        'interlocutors': [
            {'id': 'requester-1', 'role': 'REQUESTER', 'myself': True},
            {'id': 'user-1', 'role': 'USER'},
        ],
        'messages_inlined': True,
        'messages': [
            {
                'text': {'EN': 'Message text'},
                'from': {'id': 'requester-1', 'role': 'REQUESTER', 'myself': True},
                'created': '2017-01-31T09:38:01',
            }
        ],
        'folders': ['OUTBOX'],
        'answerable': True,
        'created': '2017-01-31T09:38:01',
    }


@pytest.fixture
def compose_details_direct_map():
    return {
        'recipients_select_type': 'DIRECT',
        'recipients_ids': ['user-1', 'user-2'],
    }


@pytest.fixture
def compose_details_filter_map():
    return {
        'recipients_select_type': 'FILTER',
        'recipients_filter':  {'category': 'skill', 'key': '2022', 'operator': 'GT', 'value': 90}
    }


def test_find_message_thread(respx_mock, toloka_client, toloka_url, message_thread_base_map):

    raw_result = {'items': [message_thread_base_map], 'has_more': False}

    def message_threads(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_message_threads',
            'X-Low-Level-Method': 'find_message_threads',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            folder='OUTBOX',
            folder_ne='IMPORTANT',
            created_gte='2015-12-01T00:00:00',
            created_lt='2016-06-01T00:00:00',
            sort='-created',
        ) == request.url.params
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.get(f'{toloka_url}/message-threads').mock(side_effect=message_threads)

    # Request object syntax
    request = client.search_requests.MessageThreadSearchRequest(
        folder=client.message_thread.Folder.OUTBOX,
        folder_ne=client.message_thread.Folder.IMPORTANT,
        created_gte=datetime.datetime(2015, 12, 1, tzinfo=datetime.timezone.utc),
        created_lt=datetime.datetime(2016, 6, 1, tzinfo=datetime.timezone.utc),
    )
    sort = client.search_requests.MessageThreadSortItems(['-created'])
    result = toloka_client.find_message_threads(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_message_threads(
        folder=client.message_thread.Folder.OUTBOX,
        folder_ne=client.message_thread.Folder.IMPORTANT,
        created_gte=datetime.datetime(2015, 12, 1, tzinfo=datetime.timezone.utc),
        created_lt=datetime.datetime(2016, 6, 1, tzinfo=datetime.timezone.utc),
        sort=['-created'],
    )
    assert raw_result == client.unstructure(result)


def test_get_message_threads(respx_mock, toloka_client, toloka_url, message_thread_base_map):

    threads = [dict(message_thread_base_map, id=f'message-thread-{i}') for i in range(50)]
    threads.sort(key=itemgetter('id'))

    def get_message_threads(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_message_threads',
            'X-Low-Level-Method': 'find_message_threads',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params.get('id_gt', None)
        params = params.remove('id_gt')
        assert QueryParams(
            folder='OUTBOX',
            folder_ne='IMPORTANT',
            created_gte='2015-12-01T00:00:00',
            created_lt='2016-06-01T00:00:00',
            sort='id',
        ) == params

        items = [thread for thread in threads if id_gt is None or thread['id'] > id_gt][:3]
        return httpx.Response(json={'items': items, 'has_more': items[-1]['id'] != threads[-1]['id']}, status_code=200)

    respx_mock.get(f'{toloka_url}/message-threads').mock(side_effect=get_message_threads)

    # Request object syntax
    request = client.search_requests.MessageThreadSearchRequest(
        folder=client.message_thread.Folder.OUTBOX,
        folder_ne=client.message_thread.Folder.IMPORTANT,
        created_gte=datetime.datetime(2015, 12, 1, tzinfo=datetime.timezone.utc),
        created_lt=datetime.datetime(2016, 6, 1, tzinfo=datetime.timezone.utc),
    )
    result = toloka_client.get_message_threads(request)
    assert threads == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_message_threads(
        folder=client.message_thread.Folder.OUTBOX,
        folder_ne=client.message_thread.Folder.IMPORTANT,
        created_gte=datetime.datetime(2015, 12, 1, tzinfo=datetime.timezone.utc),
        created_lt=datetime.datetime(2016, 6, 1, tzinfo=datetime.timezone.utc),
    )
    assert threads == client.unstructure(list(result))


@pytest.mark.parametrize(
    ['raw_result', 'folder', 'folder_ne'],
    [
        ({'folder': 'OUTBOX', 'folder_ne': 'IMPORTANT'}, client.message_thread.Folder.OUTBOX, client.message_thread.Folder.IMPORTANT),
        ({'folder': 'OUTBOX', 'folder_ne': 'IMPORTANT'}, 'OUTBOX', 'IMPORTANT'),
        ({'folder': 'OUTBOX'}, 'OUTBOX', None),
        (
            {'folder': 'INBOX,UNREAD', 'folder_ne': 'IMPORTANT,AUTOMATIC_NOTIFICATION'},
            [client.message_thread.Folder.INBOX, client.message_thread.Folder.UNREAD],
            [client.message_thread.Folder.IMPORTANT, client.message_thread.Folder.AUTOMATIC_NOTIFICATION],
        ),
        (
            {'folder': 'INBOX,UNREAD', 'folder_ne': 'IMPORTANT,AUTOMATIC_NOTIFICATION'},
            ['INBOX', 'UNREAD'],
            ['IMPORTANT', 'AUTOMATIC_NOTIFICATION'],
        ),
        (
            {'folder': 'INBOX,UNREAD', 'folder_ne': 'IMPORTANT,AUTOMATIC_NOTIFICATION'},
            'INBOX, UNREAD',
            'IMPORTANT, AUTOMATIC_NOTIFICATION',
        ),
    ]
)
def test_message_thread_search_request(folder, folder_ne, raw_result):
    request = client.search_requests.MessageThreadSearchRequest(folder=folder, folder_ne=folder_ne)
    assert client.unstructure(request) == raw_result

    request = client.search_requests.MessageThreadSearchRequest()
    request.folder = folder
    request.folder_ne = folder_ne
    assert client.unstructure(request) == raw_result


def test_compose_thread_direct(respx_mock, toloka_client, toloka_url, message_thread_base_map, compose_details_direct_map):
    raw_request = {
        'topic': {'EN': 'Message title'},
        'text': {'EN': 'Message text'},
        **compose_details_direct_map
    }
    raw_result = {**message_thread_base_map, 'compose_details': compose_details_direct_map}

    def message_threads(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'compose_message_thread',
            'X-Low-Level-Method': 'compose_message_thread',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=201)

    respx_mock.post(f'{toloka_url}/message-threads/compose').mock(side_effect=message_threads)

    # Request object syntax
    request = client.structure(raw_request, client.message_thread.MessageThreadCompose)
    result = toloka_client.compose_message_thread(request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.compose_message_thread(
        topic={'EN': 'Message title'},
        text={'EN': 'Message text'},
        recipients_select_type=client.message_thread.RecipientsSelectType.DIRECT,
        recipients_ids=['user-1', 'user-2'],
    )
    assert raw_result == client.unstructure(result)


def test_compose_thread_filter(respx_mock, toloka_client, toloka_url, message_thread_base_map, compose_details_filter_map):
    raw_request = {
        'topic': {'EN': 'Message title'},
        'text': {'EN': 'Message text'},
        **compose_details_filter_map
    }
    expected_request = deepcopy(raw_request)
    expected_request['recipients_filter'] = {'and': [expected_request['recipients_filter']]}
    raw_result = {**message_thread_base_map, 'compose_details': compose_details_filter_map}

    def message_threads(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'compose_message_thread',
            'X-Low-Level-Method': 'compose_message_thread',
        }
        check_headers(request, expected_headers)

        assert expected_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=201)

    respx_mock.post(f'{toloka_url}/message-threads/compose').mock(side_effect=message_threads)

    # Request object syntax
    request = client.structure(raw_request, client.message_thread.MessageThreadCompose)
    result = toloka_client.compose_message_thread(request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.compose_message_thread(
        topic={'EN': 'Message title'},
        text={'EN': 'Message text'},
        recipients_select_type=client.message_thread.RecipientsSelectType.FILTER,
        # TODO: do we really need this And?
        recipients_filter=client.filter.FilterAnd([client.filter.Skill('2022') > 90])
    )
    assert raw_result == client.unstructure(result)


def test_reply_message_thread(respx_mock, toloka_client, toloka_url, message_thread_base_map):
    raw_request = {'text': {'EN': 'Message text'}}

    def message_threads(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'reply_message_thread',
            'X-Low-Level-Method': 'reply_message_thread',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=message_thread_base_map, status_code=200)

    respx_mock.post(f'{toloka_url}/message-threads/42/reply').mock(side_effect=message_threads)

    reply = client.structure(raw_request, client.message_thread.MessageThreadReply)
    result = toloka_client.reply_message_thread('42', reply)
    assert message_thread_base_map == client.unstructure(result)


def test_add_message_thread_to_folders(respx_mock, toloka_client, toloka_url, message_thread_base_map):
    raw_request = {'folders': ['IMPORTANT']}

    def message_threads(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'add_message_thread_to_folders',
            'X-Low-Level-Method': 'add_message_thread_to_folders',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=message_thread_base_map, status_code=200)

    respx_mock.post(f'{toloka_url}/message-threads/42/add-to-folders').mock(side_effect=message_threads)

    # Request object syntax
    request = client.structure(raw_request, client.message_thread.MessageThreadFolders)
    result = toloka_client.add_message_thread_to_folders('42', request)
    assert message_thread_base_map == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.add_message_thread_to_folders('42', folders=[client.message_thread.Folder.IMPORTANT])
    assert message_thread_base_map == client.unstructure(result)


def test_remove_message_thread_from_folders(respx_mock, toloka_client, toloka_url, message_thread_base_map):
    raw_request = {'folders': ['UNREAD']}

    def message_threads(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'remove_message_thread_from_folders',
            'X-Low-Level-Method': 'remove_message_thread_from_folders',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=message_thread_base_map, status_code=200)

    respx_mock.post(f'{toloka_url}/message-threads/42/remove-from-folders').mock(side_effect=message_threads)

    # Request object syntax
    request = client.structure(raw_request, client.message_thread.MessageThreadFolders)
    result = toloka_client.remove_message_thread_from_folders('42', request)
    assert message_thread_base_map == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.remove_message_thread_from_folders('42', folders=[client.message_thread.Folder.UNREAD])
    assert message_thread_base_map == client.unstructure(result)
