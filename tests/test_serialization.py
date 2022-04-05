import datetime

import pytest
from toloka.client._converter import unstructure, structure


@pytest.mark.parametrize(
    'to_unstructure, result',
    [
        (datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc), '2022-01-01T00:00:00'),
        (datetime.datetime(2022, 1, 1, tzinfo=None), '2022-01-01T00:00:00'),
        (datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=-3))), '2022-01-01T03:00:00'),
    ]
)
def test_time_format_unstructure(to_unstructure, result):
    assert unstructure(to_unstructure) == result


@pytest.mark.parametrize(
    'to_structure, result',
    [
        ('2022-01-01T00:00:00', datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc)),
        ('2022-01-01T00:00:00+00:00', datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc)),
        ('2022-01-01T03:00:00', datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=-3)))),
        (datetime.datetime(2022, 1, 1, tzinfo=None), datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc)),
        (datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc), datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc)),
    ]
)
def test_time_format_structure(to_structure, result):
    assert structure(to_structure, datetime.datetime) == result
