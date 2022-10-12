import json
import requests
from toloka.client.filter import Languages


def test_all_verified_languages_skills_exist(client):
    skills = Languages.VERIFIED_LANGUAGES_TO_SKILLS.values()
    for skill in skills:
        assert client.get_skill(skill).id == skill


def test_verified_languages_to_skills_mapping_is_up_to_date():
    local_mapping = Languages.VERIFIED_LANGUAGES_TO_SKILLS
    remote_mapping = json.loads(requests.get('https://toloka.dev/api/env').content)['config']['public_verifiedLanguages']
    remote_keys = remote_mapping[::2]  # every first element in list
    remote_values = remote_mapping[1::2]  # every second element in list
    remote_mapping = dict(zip(remote_keys, remote_values))
    assert local_mapping == remote_mapping
