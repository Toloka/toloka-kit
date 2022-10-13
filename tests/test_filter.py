import datetime
import pickle
import copy
import pytest
from toloka.client.filter import Languages, FilterAnd, FilterOr, Skill, Gender, OSVersion, Verified
from toloka.client.pool import Pool


def test_simple_language():
    assert Languages.in_('EN').unstructure() == {
        'operator': 'IN',
        'value': 'EN',
        'key': 'languages',
        'category': 'profile'
    }
    assert Languages.not_in('EN').unstructure() == {
        'operator': 'NOT_IN',
        'value': 'EN',
        'key': 'languages',
        'category': 'profile'
    }


def test_language_multiple():
    assert Languages.in_(['EN', 'RU']) == (Languages.in_('EN') | Languages.in_('RU'))
    assert Languages.not_in(['EN', 'RU']) == (Languages.not_in('EN') & Languages.not_in('RU'))


def test_verified_language():
    assert Languages.in_('EN', verified=True) == FilterOr([
        Languages.in_('EN') & Skill('26366').eq(100)
    ])


def test_verified_language_multiple():
    assert Languages.in_(['EN', 'RU'], verified=True) == (
        (Languages.in_('EN') & Skill('26366').eq(100)) |
        (Languages.in_('RU') & Skill('26296').eq(100))
    )


def test_verified_language_not_in_is_incorrect():
    with pytest.raises(ValueError):
        Languages.not_in('EN', verified=True)
    with pytest.raises(ValueError):
        Languages.not_in(['RU', 'EN'], verified=True)


def test_unknown_verified_language_in_is_incorrect():
    with pytest.raises(ValueError):
        Languages.in_('fake language', verified=True)
    with pytest.raises(ValueError):
        Languages.in_(['EN', 'fake language'], verified=True)


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


@pytest.mark.parametrize('obj,obj_inverted', [
    (Languages.in_(['EN', 'RU']), Languages.not_in(['EN', 'RU'])),
    (Skill('123') == 10, Skill('123') != 10),
    (Skill('123') > 10, Skill('123') <= 10),
    (Verified == True, Verified == False)
])
def test_filter_inversion(obj, obj_inverted):
    assert ~obj == obj_inverted


@pytest.mark.parametrize('obj,obj_inverted', [
    (
        Languages.in_(['EN', 'RU']) & (Skill('123') == 10),
        Languages.not_in(['EN', 'RU']) | (Skill('123') != 10)
    ),
    (
        Languages.in_(['RU']) | ((Skill('123') > 10) & (Skill('123') <= 90)),
        Languages.not_in(['RU']) & ((Skill('123') <= 10) | (Skill('123') > 90)),
    ),
])
def test_complex_filter_inversion(obj, obj_inverted):
    assert ~obj == obj_inverted


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
    filter_with_verified_language = new_filter & Languages.in_('EN', verified=True)
    pool.filter = filter_with_verified_language
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
                ]
            },
            {
                'or': [
                    {
                        'and': [
                            {
                                'category': 'profile',
                                'key': 'languages',
                                'operator': 'IN',
                                'value': 'EN'
                            },
                            {
                                'category': 'skill',
                                'key': '26366',
                                'operator': 'EQ',
                                'value': 100.0
                            }
                        ],
                    }
                ]
            },
        ]
    }
