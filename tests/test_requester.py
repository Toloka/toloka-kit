import toloka.client as client


def test_get_requester(requests_mock, toloka_client, toloka_url):
    result = {
        'id': '566ec2b0ff0deeaae5f9d500',
        'balance': 120.3,
        'public_name': {
            'EN': 'John Smith',
            'RU': 'Джон Смит',
        },
        'company': {
            'id': '1',
            'superintendent_id': 'superintendent-1id',
        },
    }

    requests_mock.get(f'{toloka_url}/requester', json=result)
    assert result == client.unstructure(toloka_client.get_requester())
