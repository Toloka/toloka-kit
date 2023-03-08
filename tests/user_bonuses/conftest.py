from decimal import Decimal

import pytest


@pytest.fixture
def user_bonus_map():
    return {
        'user_id': 'user-1',
        'amount': Decimal('1.50'),
        'private_comment': 'pool_23214',
        'assignment_id': 'assignment-1',
        'public_title': {
            'EN': 'Good Job!',
            'RU': 'Молодец!',
        },
        'public_message': {
            'EN': 'Ten tasks completed',
            'RU': 'Выполнено 10 заданий',
        }
    }


@pytest.fixture
def user_bonus_map_without_message(user_bonus_map):
    user_bonus_map_without_message = user_bonus_map.copy()
    del user_bonus_map_without_message['public_title']
    del user_bonus_map_without_message['public_message']
    user_bonus_map_without_message['without_message'] = True
    return user_bonus_map_without_message


@pytest.fixture
def user_bonus_map_with_readonly(user_bonus_map):
    return dict(
        user_bonus_map,
        id='user-bonus-1',
        created='2016-10-23T13:27:00',
    )


@pytest.fixture
def user_bonus_map_without_message_with_readonly(user_bonus_map_without_message):
    return dict(
        user_bonus_map_without_message,
        id='user-bonus-1',
        created='2016-10-23T13:27:00',
    )
