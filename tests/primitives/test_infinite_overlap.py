import pytest

from toloka.client._converter import unstructure
from toloka.client.primitives.base import BaseTolokaObject
from toloka.client.primitives.infinite_overlap import InfiniteOverlapParametersMixin


class Parameters(InfiniteOverlapParametersMixin, BaseTolokaObject):
    payload: int


def test_constructor():

    params = Parameters(payload=None, overlap=None, infinite_overlap=None)
    assert None is unstructure(params)

    with pytest.raises(ValueError):
        Parameters(payload=None, overlap=None, infinite_overlap=False)

    params = Parameters(payload=None, overlap=None, infinite_overlap=True)
    assert {'overlap': None, 'infinite_overlap': True} == unstructure(params)

    params = Parameters(payload=None, overlap=1, infinite_overlap=None)
    assert {'overlap': 1, 'infinite_overlap': False} == unstructure(params)

    params = Parameters(payload=None, overlap=1, infinite_overlap=False)
    assert {'overlap': 1, 'infinite_overlap': False} == unstructure(params)

    with pytest.raises(ValueError):
        Parameters(payload=None, overlap=1, infinite_overlap=True)

    params = Parameters(payload=123, overlap=None, infinite_overlap=None)
    assert {'payload': 123} == unstructure(params)

    with pytest.raises(ValueError):
        Parameters(payload=123, overlap=None, infinite_overlap=False)

    params = Parameters(payload=123, overlap=None, infinite_overlap=True)
    assert {'payload': 123, 'overlap': None, 'infinite_overlap': True} == unstructure(params)

    params = Parameters(payload=123, overlap=1, infinite_overlap=None)
    assert {'payload': 123, 'overlap': 1, 'infinite_overlap': False} == unstructure(params)

    params = Parameters(payload=123, overlap=1, infinite_overlap=False)
    assert {'payload': 123, 'overlap': 1, 'infinite_overlap': False} == unstructure(params)

    with pytest.raises(ValueError):
        Parameters(payload=123, overlap=1, infinite_overlap=True)


def test_assign_overlap():
    # Assigning overlap=None
    params = Parameters(payload=123, overlap=None, infinite_overlap=None)
    with pytest.raises(ValueError):
        params.overlap = None

    params = Parameters(payload=123, overlap=None, infinite_overlap=True)
    with pytest.raises(ValueError):
        params.overlap = None

    params = Parameters(payload=123, overlap=1, infinite_overlap=False)
    with pytest.raises(ValueError):
        params.overlap = None

    # Assigning overlap=2
    params = Parameters(payload=123, overlap=None, infinite_overlap=None)
    params.overlap = 2
    assert {'payload': 123, 'overlap': 2, 'infinite_overlap': False} == unstructure(params)

    params = Parameters(payload=123, overlap=None, infinite_overlap=True)
    params.overlap = 2
    assert {'payload': 123, 'overlap': 2, 'infinite_overlap': False} == unstructure(params)

    params = Parameters(payload=123, overlap=1, infinite_overlap=False)
    params.overlap = 2
    assert {'payload': 123, 'overlap': 2, 'infinite_overlap': False} == unstructure(params)


def test_assign_infinite_overlap():
    # Assigning infinite_overlap=None
    params = Parameters(payload=123, overlap=None, infinite_overlap=None)
    with pytest.raises(ValueError):
        params.infinite_overlap = None

    params = Parameters(payload=123, overlap=None, infinite_overlap=True)
    with pytest.raises(ValueError):
        params.infinite_overlap = None

    params = Parameters(payload=123, overlap=1, infinite_overlap=False)
    with pytest.raises(ValueError):
        params.infinite_overlap = None

    # Assigning infinite_overlap=False
    params = Parameters(payload=123, overlap=None, infinite_overlap=None)
    with pytest.raises(ValueError):
        params.infinite_overlap = False

    params = Parameters(payload=123, overlap=None, infinite_overlap=True)
    with pytest.raises(ValueError):
        params.infinite_overlap = False

    params = Parameters(payload=123, overlap=1, infinite_overlap=False)
    with pytest.raises(ValueError):
        params.infinite_overlap = False

    # Assigning infinite_overlap=True
    params = Parameters(payload=123, overlap=None, infinite_overlap=None)
    params.infinite_overlap = True
    assert {'payload': 123, 'overlap': None, 'infinite_overlap': True} == unstructure(params)

    params = Parameters(payload=123, overlap=None, infinite_overlap=True)
    params.infinite_overlap = True
    assert {'payload': 123, 'overlap': None, 'infinite_overlap': True} == unstructure(params)

    params = Parameters(payload=123, overlap=1, infinite_overlap=False)
    params.infinite_overlap = True
    assert {'payload': 123, 'overlap': None, 'infinite_overlap': True} == unstructure(params)
