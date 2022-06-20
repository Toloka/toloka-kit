import json


def compare_view_specs(left, right):
    if not isinstance(left, dict):
        assert left == right
    else:
        keys = left.keys() | right.keys()
        keys.discard('_unexpected')
        keys.discard('localizationConfig')
        keys.discard('inputExample')
        for key in keys:
            # config is serialized to string so to compare two dicts serialized to strings we need to deserialize
            # them first
            if key == 'config':
                compare_view_specs(json.loads(left[key]), json.loads(right[key]))
            else:
                compare_view_specs(left[key], right[key])


def assert_view_spec_uploads_to_project(client, project, view_spec):
    project.task_spec.view_spec = view_spec
    created_project = client.update_project(project.id, project)
    compare_view_specs(created_project.task_spec.view_spec.unstructure(), view_spec.unstructure())
