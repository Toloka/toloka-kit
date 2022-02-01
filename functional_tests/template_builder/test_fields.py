import pytest

from . import assert_view_spec_uploads_to_project
from pytest_lazyfixture import lazy_fixture
from toloka.client.project import TemplateBuilderViewSpec
from toloka.client.project import template_builder as tb


@pytest.fixture
def audio_field(add_label_hint_validation):
    return add_label_hint_validation(tb.AudioFieldV1)(
        tb.OutputData('label'),
        multiple=True,
    )


@pytest.fixture
def button_radio_field(add_label_hint_validation):
    return add_label_hint_validation(tb.ButtonRadioFieldV1)(
        tb.OutputData('label'), 10
    )


@pytest.fixture
def button_radio_group_field(add_label_hint_validation):
    return add_label_hint_validation(tb.ButtonRadioGroupFieldV1)(
        tb.OutputData('label'),
        [tb.GroupFieldOption('yes', 'yes')],
    )


@pytest.fixture
def checkbox_field(add_label_hint_validation):
    return add_label_hint_validation(tb.CheckboxFieldV1)(
        tb.OutputData('label'),
        disabled=True,
        preserve_false=True,
    )


@pytest.fixture
def checkbox_group_field(add_label_hint_validation):
    return add_label_hint_validation(tb.CheckboxGroupFieldV1)(
        tb.OutputData('label'),
        [tb.GroupFieldOption('yes', 'yes')],
        disabled=True,
        preserve_false=True,
    )


@pytest.fixture
def date_field(add_label_hint_validation):
    return add_label_hint_validation(tb.DateFieldV1)(
        tb.OutputData('label'), 'date',
        block_list=['2000-01-01'],
        max=['2050-01-01'],
        min=['1000-01-01'],
        placeholder='this is placeholder',
    )


@pytest.fixture
def email_field(add_label_hint_validation):
    return add_label_hint_validation(tb.EmailFieldV1)(
        tb.OutputData('label'),
        placeholder='this is placeholder',
    )


@pytest.fixture
def file_field(add_label_hint_validation):
    return add_label_hint_validation(tb.FileFieldV1)(
        tb.OutputData('label'),
        ['image/png'],
        multiple=True,
    )


@pytest.fixture
def image_annotation_field(add_label_hint_validation):
    return add_label_hint_validation(tb.ImageAnnotationFieldV1)(
        tb.OutputData('label'),
        'fake_image_path',
        disabled=True,
        full_height=True,
        labels=[tb.ImageAnnotationFieldV1.Label('yes', 'yes')],
        min_width=300.,
        ratio=[1., 2.],
        shapes={
            'point': True,
            'polygon': True,
            'rectangle': True,
        },
    )


@pytest.fixture
def list_field(add_label_hint_validation):
    return add_label_hint_validation(tb.ListFieldV1)(
        tb.OutputData('label'),
        tb.TextFieldV1(
            data=tb.RelativeData()
        ),
        button_label='button label',
        direction='vertical',
        editable=True,
        max_length=3.,
        size='s',
    )


@pytest.fixture
def media_file_field(add_label_hint_validation):
    return add_label_hint_validation(tb.MediaFileFieldV1)(
        tb.OutputData('label'),
        tb.MediaFileFieldV1.Accept(
            file_system=True,
            gallery=True,
            photo=True,
            video=True,
        ),
        multiple=True,
    )


@pytest.fixture
def number_field(add_label_hint_validation):
    return add_label_hint_validation(tb.NumberFieldV1)(
        tb.OutputData('label'),
        maximum=100,
        minimum=-100,
        placeholder='placeholder',
    )


@pytest.fixture
def phone_number_field(add_label_hint_validation):
    return add_label_hint_validation(tb.PhoneNumberFieldV1)(
        tb.OutputData('label'),
        placeholder='placeholder',
    )


@pytest.fixture
def radio_group_field(add_label_hint_validation):
    return add_label_hint_validation(tb.RadioGroupFieldV1)(
        tb.OutputData('label'),
        [tb.GroupFieldOption('yes', 'yes')],
        disabled=True,
    )


@pytest.fixture
def select_field(add_label_hint_validation):
    return add_label_hint_validation(tb.SelectFieldV1)(
        tb.OutputData('label'),
        [tb.SelectFieldV1.Option(label='yes', value='yes')],
        placeholder='placeholder',
    )


@pytest.fixture
def text_field(add_label_hint_validation):
    return add_label_hint_validation(tb.TextFieldV1)(
        tb.OutputData('label'),
        disabled=True,
        placeholder='placeholder',
    )


@pytest.fixture
def text_annotation_field(add_label_hint_validation):
    return add_label_hint_validation(tb.TextAnnotationFieldV1)(
        tb.OutputData('label'),
        adjust='words',
        content='this is content',
        disabled=True,
        labels=[tb.TextAnnotationFieldV1.Label('yes', 'yes')],
    )


@pytest.fixture
def textarea_field(add_label_hint_validation):
    return add_label_hint_validation(tb.TextareaFieldV1)(
        tb.OutputData('label'),
        disabled=True,
        placeholder='placeholder',
        resizable=False,
        rows=3.,
    )


@pytest.mark.parametrize(
    'field_component', [
        lazy_fixture('audio_field'),
        lazy_fixture('button_radio_field'),
        lazy_fixture('button_radio_group_field'),
        lazy_fixture('checkbox_field'),
        lazy_fixture('checkbox_group_field'),
        lazy_fixture('date_field'),
        lazy_fixture('email_field'),
        lazy_fixture('file_field'),
        lazy_fixture('image_annotation_field'),
        lazy_fixture('list_field'),
        lazy_fixture('media_file_field'),
        lazy_fixture('number_field'),
        lazy_fixture('phone_number_field'),
        lazy_fixture('radio_group_field'),
        lazy_fixture('select_field'),
        lazy_fixture('text_field'),
        lazy_fixture('text_annotation_field'),
        lazy_fixture('textarea_field'),
    ]
)
def test_field_component(field_component, client, empty_project):
    view_spec = TemplateBuilderViewSpec(
        view=tb.ListViewV1(
            items=[field_component]
        )
    )
    assert_view_spec_uploads_to_project(
        client, empty_project, view_spec
    )
