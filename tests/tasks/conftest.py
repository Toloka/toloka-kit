import pytest


@pytest.fixture
def task_map():
    return {
        'pool_id': '21',
        'input_values': {'image': 'http://images.com/1.png'},
        'known_solutions': [
            {
                'output_values': {'color': 'white'},
                'correctness_weight': 1.0,
            },
            {
                'output_values': {'color': 'gray'},
                'correctness_weight': 0.71,
            },
        ],
        'message_on_unknown_solution': 'Main color is white',
        'baseline_solutions': [
            {
                'output_values': {'color': 'white'},
                'confidence_weight': 1.0,
            },
            {
                'output_values': {'color': 'gray'},
                'confidence_weight': 0.71,
            },
        ],
        'overlap': 3,
        'infinite_overlap': False,
        'remaining_overlap': 3,
        'unavailable_for': ['user-1id'],
        'reserved_for': ['user-2id'],
        'traits_all_of': ['trait-1'],
        'traits_any_of': ['trait-2'],
        'traits_none_of_any': ['trait-3'],
    }


@pytest.fixture
def task_map_with_readonly(task_map):
    return {**task_map, 'created': '2016-10-09T11:42:01'}
