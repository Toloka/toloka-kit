import datetime
import pickle
import copy
import pytest
from toloka.client.filter import Languages, FilterAnd, Skill, Gender, OSVersion
from toloka.client.pool import Pool


def test_simple_language():
    assert Languages.in_('EN').unstructure() == {'operator': 'IN', 'value': 'EN', 'key': 'languages', 'category': 'profile'}


def test_verified_language_not_in_is_incorrect():
    with pytest.raises(ValueError):
        Languages.not_in('EN', verified=True)


def test_unknown_verified_language_is_incorrect():
    with pytest.raises(ValueError):
        Languages.in_(['fake language 1', 'EN'], verified=True)


def test_language_multiple():
    assert Languages.in_('EN', verified=True) == FilterAnd([Languages.in_('EN'), Skill('26366').eq(100)])


def test_verified_language_multiple():
    assert Languages.in_(['EN', 'RU'], verified=True) == FilterAnd([Languages.in_(['EN', 'RU']), Skill('26366').eq(100), Skill('26296').eq(100)])


@pytest.mark.parametrize(
    'obj', [Languages.in_(['EN', 'RU'], verified=True), Languages.in_(['EN', 'RU'])]
)
def test_language_pickleable(obj):
    assert obj == pickle.loads(pickle.dumps(obj))


@pytest.mark.parametrize(
    'obj', [Languages.in_(['EN', 'RU'], verified=True), Languages.in_(['EN', 'RU'])]
)
def test_language_deepcopyable(obj):
    assert obj == copy.deepcopy(obj)

# ((filter.Gender == filter.Gender.FEMALE) | (filter.Country != 'BE')) &
# (filter.Citizenship == 'BY') &
# (filter.Education == filter.Education.MIDDLE) &
# (filter.AdultAllowed == True) &  # noqa: E712
# (filter.DateOfBirth > 604972800) &
# (filter.City.not_in(225)) &
# (filter.Languages.in_('RU')) &
# (filter.RegionByPhone.in_(213) & filter.RegionByIp.not_in(1)) &
# (filter.DeviceCategory == filter.DeviceCategory.PERSONAL_COMPUTER) &
# (filter.OSFamily == filter.OSFamily.WINDOWS) &
# (filter.OSVersion >= 8.1) &
# (filter.OSVersionMajor > 8) &
# (filter.OSVersionMinor >= 1) &
# (filter.OSVersionBugfix <= 225) &
# (filter.UserAgentType == filter.UserAgentType.BROWSER) &
# (filter.UserAgentVersion < 11.12) &
# (filter.UserAgentVersionMajor < 11) &
# (filter.UserAgentVersionMinor < 12) &
# (filter.UserAgentVersionBugfix > 2026) &
# ((filter.Skill('224') >= 85) | (filter.Skill('300') != None) | (filter.Skill('350') == 75.512))  # noqa: E711

def test_filter_in_pool():
    pool = Pool(
        project_id='1234',
        private_name='Pool 1',
        may_contain_adult_content=False,
        will_expire=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365),
        reward_per_assignment=0.01,
        assignment_max_duration_seconds=60*20,
        defaults=Pool.Defaults(default_overlap_for_new_task_suites=3),
        filter=Languages.in_('EN'),
    )
    new_filter = (Gender == Gender.FEMALE)
    pool.filter = new_filter
    assert pool.unstructure()['filter'] == {
        'and': [
            {
                'or': [
                    {
                        'category': 'profile',
                        'key': 'gender',
                        'operator': 'EQ',
                        'value': 'FEMALE'
                    }
                ]
            }
        ]
    }
    new_filter |= ((Skill('224') >= 85) & (OSVersion >= 8.1))
    pool.filter = new_filter
    assert pool.unstructure()['filter'] == {
        'and': [
            {
                'or': [
                    {
                        'category': 'profile',
                        'key': 'gender',
                        'operator': 'EQ',
                        'value': 'FEMALE'
                    },
                    {
                        'and': [
                            {
                                'or': [{
                                    'category': 'skill',
                                    'key': '224',
                                    'operator': 'GTE',
                                    'value': 85
                                }]
                            },
                            {
                                'or': [{
                                    'category': 'computed',
                                    'key': 'os_version',
                                    'operator': 'GTE',
                                    'value': 8.1
                                }]
                            }
                    ]
                    }
                ]
            },
        ]
    }