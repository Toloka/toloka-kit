import pytest
import pickle
from toloka.client.primitives.base import BaseTolokaObject


@pytest.fixture()
def base_toloka_object():
    obj = BaseTolokaObject()
    obj._unexpected = {'unknown_field': 'unknown_value'}
    return obj


def test_base_toloka_object_is_pickle_serializable(base_toloka_object):
    deserialized = pickle.loads(pickle.dumps(base_toloka_object))
    assert deserialized == base_toloka_object
