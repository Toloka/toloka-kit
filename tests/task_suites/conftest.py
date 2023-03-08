import pytest


@pytest.fixture
def task_suite_map():
    return {
        'pool_id': '21',
        'tasks': [
            {
                'input_values': {'image': 'http://images.com/1.png'}
            },
            {
                'input_values': {'image': 'http://images.com/2.png'},
                'known_solutions': [
                    {
                        'output_values': {'color': 'white'},
                        'correctness_weight': 1.0,
                    },
                    {
                        'output_values': {'color': 'gray'},
                        'correctness_weight': 0.71,
                    }
                ],
                'message_on_unknown_solution': 'Main color is white',
            }
        ],
        'overlap': 5,
        'infinite_overlap': False,
        'remaining_overlap': 5,
        'issuing_order_override': 10.3,
        'unavailable_for': ['tlk-user-i1d', 'tlk-user-i2d'],
        'reserved_for': ['tlk-user-i3d', 'tlk-user-i4d'],
        'traits_all_of': ['trait-1'],
        'traits_any_of': ['trait-2'],
        'traits_none_of_any': ['trait-3'],
        'longitude': 136.22,
        'latitude': 58.588,
    }


@pytest.fixture
def task_suite_map_with_readonly(task_suite_map):
    return {
        **task_suite_map,
        'id': 'task-suite-i1d',
        'mixed': False,
        'automerged': True,
        'created': '2015-12-13T23:57:12',
    }
