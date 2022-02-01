import pytest
import functools


from toloka.client.project import template_builder as tb


@pytest.fixture
def add_label_hint_validation(empty_condition):
    def func(cls):
        return functools.partial(
            cls,
            hint='hint',
            label='label',
            validation=empty_condition,
        )

    return func


@pytest.fixture
def empty_condition():
    return tb.EmptyConditionV1(
        tb.InputData('url'),
        hint='hint'
    )


@pytest.fixture
def text_view(add_label_hint_validation):
    return add_label_hint_validation(tb.TextViewV1)(
        'Hello world',
    )


@pytest.fixture
def notify_action():
    return tb.NotifyActionV1(
        tb.NotifyActionV1.Payload(
            content='Hello World!',
            theme='info',
            delay=100,
            duration=100,
        ),
    )
