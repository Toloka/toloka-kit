import datetime
from operator import itemgetter
from os import path
from urllib.parse import urlparse, parse_qs

import pytest
import toloka.client as client

from .testutils.util_functions import check_headers


@pytest.fixture
def assignment_attachment_map():
    return {
        'id': 'assignment-attachment-1',
        'owner': {
            'id': 'requester-1',
            'myself': True,
            'company_id': 'company-1',
        },
        'attachment_type': 'ASSIGNMENT_ATTACHMENT',
        'name': 'ExampleAttachment.txt',
        'media_type': 'application/octet-stream',
        'details': {
            'user_id': 'user-1',
            'assignment_id': 'assignment-1',
            'pool_id': 'pool-1',
        },
        'created': '2016-05-25T16:15:27.748000',
    }


def test_find_attachments(requests_mock, toloka_client, toloka_url, assignment_attachment_map):
    raw_result = {'items': [assignment_attachment_map], 'has_more': True}

    def attachments(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_attachments',
            'X-Low-Level-Method': 'find_attachments',
        }
        check_headers(request, expected_headers)

        assert {
            'type': ['ASSIGNMENT_ATTACHMENT'],
            'owner_id': ['requester-1'],
            'owner_company_id': ['company-1'],
            'name': ['ExampleAttachment.txt'],
            'user_id': ['user-1'],
            'created_gt': ['2000-01-01T12:57:01'],
            'sort': ['id'],
            'limit': ['50'],
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(f'{toloka_url}/attachments', json=attachments, status_code=200)

    # Request object syntax
    request = client.search_requests.AttachmentSearchRequest(
        type=client.Attachment.ASSIGNMENT_ATTACHMENT,
        owner_id='requester-1',
        owner_company_id='company-1',
        name='ExampleAttachment.txt',
        user_id='user-1',
        created_gt=datetime.datetime(2000, 1, 1, 12, 57, 1),
    )
    sort = client.search_requests.AttachmentSortItems(['id'])
    result = toloka_client.find_attachments(request, sort=sort, limit=50)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_attachments(
        type=client.Attachment.ASSIGNMENT_ATTACHMENT,
        owner_id='requester-1',
        owner_company_id='company-1',
        name='ExampleAttachment.txt',
        user_id='user-1',
        created_gt=datetime.datetime(2000, 1, 1, 12, 57, 1),
        sort=['id'],
        limit=50
    )
    assert raw_result == client.unstructure(result)


def test_get_attachments(requests_mock, toloka_client, toloka_url, assignment_attachment_map):
    attachments = [dict(assignment_attachment_map, id=f'assignment-attachment-{i}') for i in range(50)]
    attachments.sort(key=itemgetter('id'))

    def get_attachments(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_attachments',
            'X-Low-Level-Method': 'find_attachments',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0] if 'id_gt' in params else None
        assert {
            'type': ['ASSIGNMENT_ATTACHMENT'],
            'owner_id': ['requester-1'],
            'owner_company_id': ['company-1'],
            'name': ['ExampleAttachment.txt'],
            'user_id': ['user-1'],
            'created_gt': ['2000-01-01T12:57:01'],
            'sort': ['id'],
        } == params

        items = [attachment for attachment in attachments if id_gt is None or attachment['id'] > id_gt][:3]
        return {'items': items, 'has_more': items[-1]['id'] != attachments[-1]['id']}

    requests_mock.get(f'{toloka_url}/attachments', json=get_attachments, status_code=200)

    # Request object syntax
    request = client.search_requests.AttachmentSearchRequest(
        type=client.Attachment.ASSIGNMENT_ATTACHMENT,
        owner_id='requester-1',
        owner_company_id='company-1',
        name='ExampleAttachment.txt',
        user_id='user-1',
        created_gt=datetime.datetime(2000, 1, 1, 12, 57, 1),
    )
    result = toloka_client.get_attachments(request)
    assert attachments == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_attachments(
        type=client.Attachment.ASSIGNMENT_ATTACHMENT,
        owner_id='requester-1',
        owner_company_id='company-1',
        name='ExampleAttachment.txt',
        user_id='user-1',
        created_gt=datetime.datetime(2000, 1, 1, 12, 57, 1),
    )
    assert attachments == client.unstructure(list(result))


def test_get_attachment(requests_mock, toloka_client, toloka_url, assignment_attachment_map):

    def get_attachment(request,  context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_attachment',
            'X-Low-Level-Method': 'get_attachment',
        }
        check_headers(request, expected_headers)

        return assignment_attachment_map

    requests_mock.get(
        f'{toloka_url}/attachments/attachment-1',
        json=get_attachment,
        status_code=200
    )

    assert assignment_attachment_map == client.unstructure(toloka_client.get_attachment('attachment-1'))


def test_download_attachment_binary(requests_mock, toloka_client, toloka_url, tmp_path):
    content = b''.join(i.to_bytes(i.bit_length(), 'big') for i in range(1000))

    def get_content(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'download_attachment',
            'X-Low-Level-Method': 'download_attachment',
        }
        check_headers(request, expected_headers)

        return content

    requests_mock.get(
        f'{toloka_url}/attachments/attachment-i1d/download',
        content=get_content,
        headers={
            'Content-Type': 'image/png',
            'Content-Disposition': 'attachment',
        },
        status_code=200
    )

    tmp_file_path = path.join(tmp_path, 'download_attachment_result')
    with open(tmp_file_path, 'wb') as out_f:
        toloka_client.download_attachment('attachment-i1d', out_f)

    with open(tmp_file_path, 'rb') as in_f:
        assert content == in_f.read()


def test_download_attachment_text(requests_mock, toloka_client, toloka_url, tmp_path):
    content = """In a hole in the ground there lived a hobbit.
Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare,
sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort."""

    def get_content(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'download_attachment',
            'X-Low-Level-Method': 'download_attachment',
        }
        check_headers(request, expected_headers)

        return content

    requests_mock.get(
        f'{toloka_url}/attachments/attachment-i1d/download',
        text=get_content,
        headers={
            'Content-Type': 'text/html',
            'Content-Disposition': 'attachment',
        },
        status_code=200
    )

    tmp_file_path = path.join(tmp_path, 'download_attachment_result')
    with open(tmp_file_path, 'wb') as out_f:
        toloka_client.download_attachment('attachment-i1d', out_f)

    with open(tmp_file_path, 'r') as in_f:
        assert content == in_f.read()
