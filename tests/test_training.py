import datetime
import logging
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import pytest
import toloka.client as client


@pytest.fixture
def training_map():
    return {
        'project_id': '10',
        'private_name': 'training_v12_231',
        'may_contain_adult_content': True,
        'mix_tasks_in_creation_order': True,
        'shuffle_tasks_in_task_suite': True,
        'training_tasks_in_task_suite_count': 3,
        'task_suites_required_to_pass': 5,
        'retry_training_after_days': 1,
        'inherited_instructions': True,
        'metadata': {'testKey': ['testValue']},
        'assignment_max_duration_seconds': 600,
        'public_instructions': 'text'
    }


@pytest.fixture
def training_map_with_readonly(training_map):
    return {
        **training_map,
        'id': '21',
        'owner': {'id': 'requester-1', 'myself': True, 'company_id': '1'},
        'created': '2015-12-16T12:55:01',
        'last_started': '2015-12-17T08:00:01',
        'last_stopped': '2015-12-18T08:00:01',
        'last_close_reason': 'MANUAL',
        'status': 'CLOSED',
    }


@pytest.fixture
def open_training_map_with_readonly(training_map_with_readonly):
    return {
        **training_map_with_readonly,
        'status': 'OPEN'
    }


@pytest.fixture
def archived_training_map_with_readonly(training_map_with_readonly):
    return {
        **training_map_with_readonly,
        'status': 'ARCHIVED'
    }


def test_find_trainings(requests_mock, toloka_client, toloka_url, training_map_with_readonly):
    raw_result = {'items': [training_map_with_readonly], 'has_more': False}

    def trainings(request, context):
        assert {
            'project_id': ['10'],
            'id_gt': ['20'],
            'last_started_lt': ['2016-03-23T12:59:00'],
            'sort': ['created,-id'],
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(f'{toloka_url}/trainings', json=trainings)

    # Request object syntax
    request = client.search_requests.TrainingSearchRequest(
        project_id='10',
        id_gt='20',
        last_started_lt=datetime.datetime(2016, 3, 23, 12, 59, 0),
    )
    sort = client.search_requests.TrainingSortItems(['created', '-id'])
    result = toloka_client.find_trainings(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_trainings(
        project_id='10',
        id_gt='20',
        last_started_lt=datetime.datetime(2016, 3, 23, 12, 59, 0),
        sort=['created', '-id'],
    )
    assert raw_result == client.unstructure(result)


def test_get_trainings(requests_mock, toloka_client, toloka_url, training_map_with_readonly):
    trainings = [dict(training_map_with_readonly, id=str(i)) for i in range(100)]
    trainings.sort(key=itemgetter('id'))
    expected_trainings = [training for training in trainings if training['id'] > '20']

    def get_trainings(request, context):
        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0]
        assert {
            'project_id': ['10'],
            'last_started_lt': ['2016-03-23T12:59:00'],
            'sort': ['id'],
        } == params

        items = [training for training in trainings if id_gt is None or training['id'] > id_gt][:3]
        return {'items': items, 'has_more': items[-1]['id'] != trainings[-1]['id']}

    requests_mock.get(f'{toloka_url}/trainings', json=get_trainings)

    # Request object syntax
    request = client.search_requests.TrainingSearchRequest(
        project_id='10',
        id_gt='20',
        last_started_lt=datetime.datetime(2016, 3, 23, 12, 59, 0),
    )
    result = toloka_client.get_trainings(request)
    assert expected_trainings == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_trainings(
        project_id='10',
        id_gt='20',
        last_started_lt=datetime.datetime(2016, 3, 23, 12, 59, 0),
    )
    assert expected_trainings == client.unstructure(list(result))


def test_get_training(requests_mock, toloka_client, toloka_url, training_map_with_readonly):
    requests_mock.get(f'{toloka_url}/trainings/21', json=training_map_with_readonly)
    assert training_map_with_readonly == client.unstructure(toloka_client.get_training('21'))


def test_create_training(requests_mock, toloka_client, toloka_url, training_map, training_map_with_readonly, caplog):

    def trainings(request, context):
        assert training_map == request.json()
        return training_map_with_readonly

    requests_mock.post(f'{toloka_url}/trainings', json=trainings, status_code=201)
    training = client.structure(training_map, client.training.Training)
    with caplog.at_level(logging.INFO):
        caplog.clear()
        result = toloka_client.create_training(training)
        assert caplog.record_tuples == [(
            'toloka.client',
            logging.INFO,
            'A new training with ID "21" has been created. Link to open in web interface: https://sandbox.toloka.yandex.com/requester/project/10/training/21'
        )]
        assert training_map_with_readonly == client.unstructure(result)


def test_update_training(requests_mock, toloka_client, toloka_url, training_map_with_readonly):
    updated_training = {
        **training_map_with_readonly,
        'private_name': 'updated name',
    }

    def trainings(request, context):
        assert updated_training == request.json()
        return updated_training

    requests_mock.put(f'{toloka_url}/trainings/21', json=trainings)
    result = toloka_client.update_training('21', client.structure(updated_training, client.training.Training))
    assert updated_training == client.unstructure(result)


@pytest.fixture
def open_operation_map():
    return {
        'id': 'open-training-op1id',
        'type': 'TRAINING.OPEN',
        'status': 'RUNNING',
        'submitted': '2016-03-07T15:47:00',
        'started': '2016-03-07T15:47:21',
        'parameters': {'training_id': '21'},
    }


@pytest.fixture
def complete_open_operation_map(open_operation_map):
    return {
        **open_operation_map,
        'status': 'SUCCESS',
        'finished': '2016-03-07T15:48:03',
    }


def test_open_training_async(requests_mock, toloka_client, toloka_url, open_operation_map, complete_open_operation_map):
    requests_mock.post(f'{toloka_url}/trainings/21/open', json=open_operation_map, status_code=202)
    requests_mock.get(
        f'{toloka_url}/operations/{open_operation_map["id"]}',
        json=complete_open_operation_map,
        status_code=200
    )

    operation = toloka_client.open_training_async('21')
    assert open_operation_map == client.unstructure(operation)

    complete_operation = toloka_client.wait_operation(operation)
    assert complete_open_operation_map == client.unstructure(complete_operation)


def test_open_training(requests_mock, toloka_client, toloka_url,
                       open_operation_map, complete_open_operation_map, training_map_with_readonly):
    requests_mock.post(f'{toloka_url}/trainings/21/open', json=open_operation_map, status_code=202)
    requests_mock.get(
        f'{toloka_url}/operations/{open_operation_map["id"]}',
        json=complete_open_operation_map,
        status_code=200
    )
    requests_mock.get(f'{toloka_url}/trainings/21', json=training_map_with_readonly, status_code=200)

    result = toloka_client.open_training('21')
    assert training_map_with_readonly == client.unstructure(result)


@pytest.fixture
def test_open_training_already_opened(requests_mock, toloka_client, toloka_url, open_training_map_with_readonly):
    requests_mock.post(f'{toloka_url}/trainings/21/open', [{'status_code': 204}])
    requests_mock.get(f'{toloka_url}/pools/21', json=open_training_map_with_readonly)
    assert toloka_client.open_training_async('21') is None
    result = toloka_client.open_training('21')
    assert open_training_map_with_readonly == client.unstructure(result)


@pytest.fixture
def close_operation_map():
    return {
        'id': 'close-training-op1id',
        'type': 'TRAINING.CLOSE',
        'status': 'RUNNING',
        'submitted': '2016-07-22T13:04:00',
        'started': '2016-07-22T13:04:01',
        'finished': '2016-07-22T13:04:02',
        'parameters': {'training_id': '21'},
    }


@pytest.fixture
def complete_close_operation_map(close_operation_map):
    return {
        **close_operation_map,
        'status': 'SUCCESS',
        'finished': '2016-03-07T15:48:03',
    }


def test_close_training_async(requests_mock, toloka_client, toloka_url, complete_close_operation_map):
    requests_mock.post(f'{toloka_url}/trainings/21/close', json=complete_close_operation_map, status_code=202)
    result = toloka_client.wait_operation(toloka_client.close_training_async('21'))
    assert complete_close_operation_map == client.unstructure(result)


def test_close_training(requests_mock, toloka_client, toloka_url,
                        close_operation_map, complete_close_operation_map, training_map_with_readonly):
    requests_mock.post(f'{toloka_url}/trainings/21/close', json=close_operation_map, status_code=202)
    requests_mock.get(
        f'{toloka_url}/operations/{close_operation_map["id"]}',
        json=complete_close_operation_map,
        status_code=200
    )
    requests_mock.get(f'{toloka_url}/trainings/21', json=training_map_with_readonly, status_code=200)

    result = toloka_client.close_training('21')
    assert training_map_with_readonly == client.unstructure(result)


def test_close_training_already_closed(requests_mock, toloka_client, toloka_url, training_map_with_readonly):
    requests_mock.post(f'{toloka_url}/trainings/21/close', [{'status_code': 204}])
    requests_mock.get(f'{toloka_url}/trainings/21', json=training_map_with_readonly)
    assert toloka_client.close_training_async('21') is None
    result = toloka_client.close_training('21')
    assert training_map_with_readonly == client.unstructure(result)


@pytest.fixture
def archive_operation_map():
    return {
        'id': 'archive-training-op1id',
        'type': 'TRAINING.ARCHIVE',
        'status': 'RUNNING',
        'submitted': '2016-07-22T13:04:00',
        'started': '2016-07-22T13:04:01',
        'finished': '2016-07-22T13:04:02',
        'parameters': {'training_id': '21'},
    }


@pytest.fixture
def complete_archive_operation_map(archive_operation_map):
    return {
        **archive_operation_map,
        'status': 'SUCCESS',
        'finished': '2016-03-07T15:48:03',
    }


def test_archive_training_async(requests_mock, toloka_client, toloka_url, complete_archive_operation_map):
    requests_mock.post(f'{toloka_url}/trainings/21/archive', json=complete_archive_operation_map, status_code=202)
    result = toloka_client.wait_operation(toloka_client.archive_training_async('21'))
    assert complete_archive_operation_map == client.unstructure(result)


def test_archive_training(requests_mock, toloka_client, toloka_url,
                          archive_operation_map, complete_archive_operation_map, training_map_with_readonly):
    requests_mock.post(f'{toloka_url}/trainings/21/archive', json=archive_operation_map, status_code=202)
    requests_mock.get(
        f'{toloka_url}/operations/{archive_operation_map["id"]}',
        json=complete_archive_operation_map,
        status_code=200
    )
    requests_mock.get(f'{toloka_url}/trainings/21', json=training_map_with_readonly, status_code=200)

    result = toloka_client.archive_training('21')
    assert training_map_with_readonly == client.unstructure(result)


def test_close_archive_training_already_archived(requests_mock, toloka_client, toloka_url,
                                                 archived_training_map_with_readonly):
    requests_mock.post(f'{toloka_url}/trainings/21/archive', [{'status_code': 204}])
    requests_mock.get(f'{toloka_url}/trainings/21', json=archived_training_map_with_readonly)
    assert toloka_client.archive_training_async('21') is None
    result = toloka_client.archive_training('21')
    assert archived_training_map_with_readonly == client.unstructure(result)


@pytest.fixture
def clone_operation_map():
    return {
        'id': 'archive-training-op1id',
        'type': 'TRAINING.CLONE',
        'status': 'RUNNING',
        'submitted': '2016-07-22T13:04:00',
        'started': '2016-07-22T13:04:01',
        'finished': '2016-07-22T13:04:02',
        'parameters': {'training_id': '21'},
    }


@pytest.fixture
def complete_clone_operation_map(clone_operation_map):
    return {
        **clone_operation_map,
        'status': 'SUCCESS',
        'finished': '2016-03-07T15:48:03',
        'details': {'training_id': '22'},
    }


@pytest.fixture
def cloned_training_map_with_readonly(training_map_with_readonly):
    return {
        **training_map_with_readonly,
        'id': '22'
    }


def test_clone_training_async(requests_mock, toloka_client, toloka_url, complete_clone_operation_map):
    requests_mock.post(f'{toloka_url}/trainings/21/clone', json=complete_clone_operation_map, status_code=202)
    result = toloka_client.wait_operation(toloka_client.clone_training_async('21'))
    assert complete_clone_operation_map == client.unstructure(result)


def test_clone_training(requests_mock, toloka_client, toloka_url,
                        clone_operation_map, complete_clone_operation_map, cloned_training_map_with_readonly, caplog):
    requests_mock.post(f'{toloka_url}/trainings/21/clone', json=clone_operation_map, status_code=202)
    requests_mock.get(
        f'{toloka_url}/operations/{clone_operation_map["id"]}',
        json=complete_clone_operation_map,
        status_code=200
    )
    requests_mock.get(f'{toloka_url}/trainings/22', json=cloned_training_map_with_readonly, status_code=200)

    with caplog.at_level(logging.INFO):
        caplog.clear()
        result = toloka_client.clone_training('21')
        assert caplog.record_tuples == [(
            'toloka.client',
            logging.INFO,
            'A new training with ID "22" has been cloned. Link to open in web interface: https://sandbox.toloka.yandex.com/requester/project/10/training/22'
        )]
        assert cloned_training_map_with_readonly == client.unstructure(result)
