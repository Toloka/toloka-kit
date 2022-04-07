import pickle
import copy
import pytest
from toloka.client.filter import Languages, FilterAnd, Skill


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
