import json
import pytest

from toloka.client.project.view_spec import ViewSpec


@pytest.mark.parametrize(
    'example_view_spec', range(10), indirect=True
)
def test_examples(example_view_spec):
    result = ViewSpec.structure(example_view_spec).unstructure()
    assert json.loads(result.pop('config'))['plugins'] == json.loads(example_view_spec.pop('config'))['plugins']
    example_view_spec.setdefault('inferDataSpec', False)
    assert result == example_view_spec
