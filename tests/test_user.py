import pytest
import toloka.client as client
from .testutils.util_functions import check_headers


@pytest.fixture
def user_map():
    return {
        "id": "123",
        "country": "EN",
        "languages": ["EN"],
        "adult_allowed": True,
        "attributes": {
            "country_by_phone": "EN",
            "country_by_ip": "EN",
            "client_type": "TOLOKA_APP",
            "user_agent_type": "OTHER",
            "device_category": "SMARTPHONE",
            "os_family": "ANDROID",
            "os_version": 6.0,
            "os_version_major": 6,
            "os_version_minor": 0,
            "os_version_bugfix": 1,
        },
    }


def test_get_user(requests_mock, toloka_client, toloka_url, user_map):
    def get_user(request, context):
        expected_headers = {
            "X-Caller-Context": "client",
            "X-Top-Level-Method": "get_user",
            "X-Low-Level-Method": "get_user",
        }
        check_headers(request, expected_headers)

        return user_map

    requests_mock.get(f"{toloka_url}/user-metadata/123", json=get_user)
    result = toloka_client.get_user("123")
    assert user_map == client.unstructure(result)
