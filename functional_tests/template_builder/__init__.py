import json


def assert_view_spec_uploads_to_project(client, project, view_spec):
    def compare_recursively(left, right):
        if not isinstance(left, dict):
            assert left == right
        else:
            keys = left.keys() | right.keys()
            keys.discard('_unexpected')
            keys.discard('localizationConfig')
            for key in keys:
                # config is serialized to string so to compare two dicts serialized to strings we need to deserialize
                # them first
                if key == 'config':
                    compare_recursively(json.loads(left[key]), json.loads(right[key]))
                else:
                    compare_recursively(left[key], right[key])

    project.task_spec.view_spec = view_spec
    created_project = client.update_project(project.id, project)
    compare_recursively(created_project.task_spec.view_spec.unstructure(), view_spec.unstructure())
