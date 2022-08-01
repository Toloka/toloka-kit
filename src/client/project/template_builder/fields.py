__all__ = [
    'BaseFieldV1',
    'AudioFieldV1',
    'ButtonRadioFieldV1',
    'GroupFieldOption',
    'ButtonRadioGroupFieldV1',
    'CheckboxFieldV1',
    'CheckboxGroupFieldV1',
    'DateFieldV1',
    'EmailFieldV1',
    'FileFieldV1',
    'ImageAnnotationFieldV1',
    'ListFieldV1',
    'MediaFileFieldV1',
    'NumberFieldV1',
    'PhoneNumberFieldV1',
    'RadioGroupFieldV1',
    'SelectFieldV1',
    'TextFieldV1',
    'TextAnnotationFieldV1',
    'TextareaFieldV1',
]
from enum import unique
from typing import List, Any, Dict

from .base import (
    BaseComponent,
    ListDirection,
    ListSize,
    ComponentType,
    BaseTemplate,
    VersionedBaseComponentMetaclass,
    base_component_or
)
from ....util._codegen import attribute
from ....util._extendable_enum import ExtendableStrEnum
from ....util._docstrings import inherit_docstrings


class BaseFieldV1Metaclass(VersionedBaseComponentMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):
        annotations = namespace.setdefault('__annotations__', {})
        if 'data' not in namespace:
            namespace['data'] = attribute()
            annotation = {'data': BaseComponent}
            annotations = {**annotation, **annotations}
        if 'hint' not in namespace:
            namespace['hint'] = attribute(kw_only=True)
            annotations['hint'] = base_component_or(Any)
        if 'label' not in namespace:
            namespace['label'] = attribute(kw_only=True)
            annotations['label'] = base_component_or(Any)
        if 'validation' not in namespace:
            namespace['validation'] = attribute(kw_only=True)
            annotations['validation'] = BaseComponent
        namespace['__annotations__'] = annotations
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class BaseFieldV1(BaseComponent, metaclass=BaseFieldV1Metaclass):
    """Fields for entering data, such as a text field or drop-down list.

    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        hint: Hint text.
        validation: Validation based on condition.
    """

    pass


@inherit_docstrings
class AudioFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_AUDIO):
    """Component for recording audio.

    Works in the mobile app. In a browser, this component opens a window for uploading an audio file.

    Attributes:
        multiple: Determines whether multiple audio files can be recorded (or uploaded):
            False (default) — forbidden.
            True — allowed.
    """

    multiple: base_component_or(Any) = attribute(kw_only=True)


@inherit_docstrings
class ButtonRadioFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_BUTTON_RADIO):
    """A component in the form of a button.

    A Toloker makes a choice by clicking on it.

    The size of the button depends on the size of the label.
    Attributes:
        value_to_set: The value of the output data when the button is clicked.
    """

    value_to_set: base_component_or(Any) = attribute(origin='valueToSet')


class GroupFieldOption(BaseTemplate):
    """Option.

    Attributes:
        value: Returned value.
        label: The text on the object.
        hint: Additional information.
    """

    value: base_component_or(Any)
    label: base_component_or(Any)
    hint: base_component_or(Any) = attribute(kw_only=True)


@inherit_docstrings
class ButtonRadioGroupFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_BUTTON_RADIO_GROUP):
    """A component with buttons that allow the Toloker to choose between the specified values.

    The minimum number of elements is one. Any type of data can be returned.

    The size of the button is determined by the length of the text on it.
    Attributes:
        options: Array of information about the buttons.

    Example:
        How to add buttons for classification task.

        >>> classification_buttons = tb.fields.ButtonRadioGroupFieldV1(
        >>>     tb.data.OutputData(path='class'),
        >>>     [
        >>>         tb.fields.GroupFieldOption('Cat', 'cat'),
        >>>         tb.fields.GroupFieldOption('Dog', 'dog'),
        >>>     ],
        >>>     validation=tb.conditions.RequiredConditionV1(hint='Choose one of the answer options'),
        >>> )
        ...
    """

    options: base_component_or(List[base_component_or(GroupFieldOption)], 'ListBaseComponentOrGroupFieldOption')  # noqa: F821


@inherit_docstrings
class CheckboxFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_CHECKBOX):
    """Checkbox.

    Attributes:
        disabled: Property that disables the component. If true, the component will not be unavailable.
        preserve_false: Property that specifies whether to return false values in the results. By default, if the
            component returns false, this result will not be added to the output. To add false to the results, specify
            "preserveFalse": true.
    """

    disabled: base_component_or(bool) = attribute(kw_only=True)
    preserve_false: base_component_or(bool) = attribute(origin='preserveFalse', kw_only=True)


@inherit_docstrings
class CheckboxGroupFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_CHECKBOX_GROUP):
    """A group of options for selecting one or more responses.

    Attributes:
        options: Options, where value is the key that the option controls, and label is the text near the option.
        disabled: If `true', the options are inactive.
        preserve_false: Property that specifies whether to return false values in the results. By default, if the
            component returns false, this result will not be added to the output. To add false to the results, specify
            "preserveFalse": true.
    """

    options: base_component_or(List[base_component_or(GroupFieldOption)], 'ListBaseComponentOrGroupFieldOption')  # noqa: F821
    disabled: base_component_or(bool) = attribute(kw_only=True)
    preserve_false: base_component_or(bool) = attribute(origin='preserveFalse', kw_only=True)


@inherit_docstrings
class DateFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_DATE):
    """A component for entering the date and time in the desired format and range.

    You can set a list of dates that the Toloker cannot select.
    Attributes:
        data: Data with values that will be processed or changed.
        format: Format of the date entered by the Toloker:
            * date-time — date and time.
            * date — date only.
        label: Label above the component.
        block_list: List of dates that the Toloker cannot select.
            * block_list[]: Date that the Toloker cannot select.
        hint: Hint text.
        max: The latest date and time in the YYYY-MM-DD hh:mm format that the Toloker can select. Where:
            * YYYY is the year.
            * MM is the month.
            * DD is the day.
            * hh is the time in hours.
            * mm is the time in minutes.
        min: The earliest date and time in the YYYY-MM-DD hh:mm format that the Toloker can select. Where:
            * YYYY is the year.
            * MM is the month.
            * DD is the day.
            * hh is the time in hours.
            * mm is the time in minutes.
        placeholder: A semi-transparent label that is shown in the box when it is empty.
        validation: Validation based on condition.
    """

    format: base_component_or(Any)
    block_list: base_component_or(List[base_component_or(Any)], 'ListBaseComponentOrAny') = attribute(  # noqa: F821
        origin='blockList',
        kw_only=True
    )
    max: base_component_or(Any) = attribute(kw_only=True)
    min: base_component_or(Any) = attribute(kw_only=True)
    placeholder: base_component_or(Any) = attribute(kw_only=True)


@inherit_docstrings
class EmailFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_EMAIL):
    """Creates a field for entering an email address.

    Checks that the text contains the @ character. You can set other conditions yourself.
    Attributes:
        placeholder: A semi-transparent label that is shown in an empty field.
    """

    placeholder: Any = attribute(kw_only=True)


@inherit_docstrings
class FileFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_FILE):
    """This component can be used for uploading files. It's displayed in the interface as an upload button.

    You can restrict the file types to upload in the "accept" property. By default, only one file can be uploaded,
    but you can allow multiple files in the "multiple" property.

    If a Toloker logs in from a mobile device, it's more convenient to use field.media-file — it's adapted for mobile
    devices and makes it easier to upload photos and videos.
    Attributes:
        accept: A list of file types that can be uploaded. By default, you can upload any files.
            Specify the types in the [certain format](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types).
            For example, you can allow only images to be uploaded by adding the image/jpeg and image/png types.
        multiple: Determines whether multiple files can be uploaded:
            * false (default) — forbidden.
            * true — allowed.
    """

    accept: base_component_or(List[base_component_or(str)], 'ListBaseComponentOrStr')  # noqa: F821
    multiple: base_component_or(bool) = attribute(kw_only=True)


@inherit_docstrings
class ImageAnnotationFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_IMAGE_ANNOTATION):
    """Adds an interface for selecting areas in images.

    If you need to select different types of objects, classify the areas using the labels property.

    You can select areas using points, polygons, and rectangles. In the shapes property, you can keep some of the
    selection modes and hide the rest.
    Attributes:
        image: The image you want to select areas in.
        disabled: Determines whether adding and deleting areas is allowed:
            * false (default) — Allowed.
            * true — Not allowed.
            You can use this feature when creating an interface to check whether the selection is correct,
             or if you need to allow selection only when a certain condition is met.
        full_height: If true, the element takes up all the vertical free space. The element is set to a minimum height
            of 400 pixels.
        labels: Used to classify areas.
            You can add several area types. When adding an area type, a button to select it appears in the interface,
            and when setting a new value, a new area selection color is added.
            This feature is instrumental if you need to select different types of objects: you can use one color to
            select cars and a different one for pedestrians.
        min_width: Minimum width of the element in pixels. Takes priority over max_width.
        ratio: An array of two numbers that sets the relative dimensions of the sides: width (first number) to height
            (second number). Not valid if full_height=true.
        shapes: Used to add and hide selection modes: points, polygons, and rectangles. All three modes are available
            by default.
            Use this property if you only need to keep certain modes. Modes with the true value are available.
    """

    class Label(BaseTemplate):
        """At least two objects must be added to the array.

        Attributes:
            label: Text on the button for selecting a selection color.
            value: The value to be written to the labels property data. Displayed to Tolokers as color options when
                selecting areas.
        """

        label: base_component_or(str)
        value: base_component_or(str)

    @unique
    class Shape(ExtendableStrEnum):
        POINT = 'point'
        POLYGON = 'polygon'
        RECTANGLE = 'rectangle'

    image: base_component_or(str)
    disabled: base_component_or(bool) = attribute(kw_only=True)
    full_height: base_component_or(bool) = attribute(origin='fullHeight', kw_only=True)
    labels: base_component_or(List[base_component_or(Label)], 'ListBaseComponentOrLabel') = attribute(kw_only=True)  # noqa: F821
    min_width: base_component_or(float) = attribute(origin='minWidth', kw_only=True)
    ratio: base_component_or(List[base_component_or(float)], 'ListBaseComponentOrFloat') = attribute(kw_only=True)  # noqa: F821
    shapes: base_component_or(Dict[base_component_or(Shape), base_component_or(bool)],
                              'DictBaseComponentOrShapeBaseComponentOrBool') = attribute(kw_only=True)  # noqa: F821


@inherit_docstrings
class ListFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_LIST):
    """A component that allows a Toloker to add and remove list items, such as text fields to fill in.

    This way you can allow a Toloker to give multiple answers to a question.

    The list items can contain any component, including a list of other components. For example, this allows you to
    create a table where you can add and delete rows.

    To add a new list item, the Toloker clicks the button. To remove an item, they click on the x on the right (it appears
    when hovering over a list item).

    To prevent a Toloker from adding too many list items, set the maximum list length. You can also use the editable
    property to block Tolokers from changing a component, like when a certain event occurs.
    Attributes:
        render: Interface template for list items, such as a text field.
            In nested field.* components, use data.relative for recording responses, otherwise all the list items will
            have the same value.
        button_label: Text on the button for adding list items.
        direction: The direction of the list.
        editable: A property that indicates whether adding and removing list items is allowed. Set false to disable.
            By default it is true (allowed).
        max_length: Maximum number of list items.
        size: The distance between list items. Acceptable values in ascending order: s, m (default).
    """

    render: BaseComponent
    button_label: base_component_or(Any) = attribute(kw_only=True)
    direction: base_component_or(ListDirection) = attribute(kw_only=True)
    editable: base_component_or(bool) = attribute(kw_only=True)
    max_length: base_component_or(float) = attribute(kw_only=True)
    size: base_component_or(ListSize) = attribute(kw_only=True)


@inherit_docstrings
class MediaFileFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_MEDIA_FILE):
    """Adds buttons for different types of uploads: uploading photos or videos, selecting files from the file manager or choosing from the gallery.
    In the accept property, select which buttons you need.

    By default, only one file can be uploaded, but you can allow multiple files in the multiple property.

    This component is convenient when using mobile devices. To upload files from a computer, it's better to use
    field.file for a more flexible configuration of the file types.
    Attributes:
        accept: Adds different buttons for four types of uploads. Pass the true value for the ones that you need.
            For example, if you need a button for uploading files from the gallery, add the "gallery": true property
        multiple: Determines whether multiple files can be uploaded:

    Example:
        How to allow Tolokers to upload images and make photos.

        >>> image_loader = tb.fields.MediaFileFieldV1(
        >>>     label='Upload a photo',
        >>>     data=tb.data.OutputData(path='image'),
        >>>     validation=tb.conditions.RequiredConditionV1(),
        >>>     accept=tb.fields.MediaFileFieldV1.Accept(photo=True, gallery=True),
        >>>     multiple=False,
        >>> )
        ...
    """

    class Accept(BaseTemplate):
        """Adds different buttons for four types of uploads.

        Attributes:
            file_system: Adds a button for uploading files from the file manager.
            gallery: Adds a button for uploading files from the gallery.
            photo: Adds a button for uploading images.
            video: Adds a button for uploading videos.
        """

        file_system: base_component_or(bool) = attribute(origin='fileSystem', kw_only=True)
        gallery: base_component_or(bool) = attribute(kw_only=True)
        photo: base_component_or(bool) = attribute(kw_only=True)
        video: base_component_or(bool) = attribute(kw_only=True)

    accept: base_component_or(Accept)
    multiple: base_component_or(bool) = attribute(kw_only=True)


@inherit_docstrings
class NumberFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_NUMBER):
    """A component that allows you to enter a number.

    The box already has validation: by default, Tolokers can enter only numbers and decimal separators. They can use either
    a dot or a comma as a separator, but there will always be a dot in the output.

    When the Toloker is entering a number, the separator automatically changes to the one specified in the regional
    settings. For Russia, the separator is a comma.

    Negative numbers are allowed by default. To disable them, use the validation property. Pressing the up or down arrow
    keys will increase or decrease the number by one.
    Attributes:
        maximum: Maximum number that can be entered.
        minimum: Minimum number that can be entered.
        placeholder: A semi-transparent label that is shown in the box when it is empty.
    """

    maximum: base_component_or(int) = attribute(kw_only=True)
    minimum: base_component_or(int) = attribute(kw_only=True)
    placeholder: base_component_or(Any) = attribute(kw_only=True)


@inherit_docstrings
class PhoneNumberFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_PHONE_NUMBER):
    """Creates a field for entering a phone number.

    Allows entering numbers, spaces, and the +, ( ), - characters. Only numbers and the + character at the beginning
    will remain in the data. For example, if you enter +7 (012) 345-67-89, the data gets the +70123456789 value.
    Attributes:
        placeholder: A semi-transparent label that is shown in an empty field.
    """

    placeholder: base_component_or(str) = attribute(kw_only=True)


@inherit_docstrings
class RadioGroupFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_RADIO_GROUP):
    """A component for selecting one value out of several options. It is designed as a group of circles arranged vertically.

    If you want it to look like normal buttons, use field.button-radio-group.

    The minimum number of buttons is one. Any type of data can be returned.
    Attributes:
        options: List of options to choose from
        disabled: This property prevents clicking the button. If the value is true, the button is not active (the Toloker
            will not be able to click it).

    Example:
        How to add label selector to interface.

        >>> radio_group_field = tb.fields.RadioGroupFieldV1(
        >>>     tb.data.OutputData(path='result'),
        >>>     [
        >>>         tb.fields.GroupFieldOption('Cat', 'cat'),
        >>>         tb.fields.GroupFieldOption('Dog', 'dog'),
        >>>     ],
        >>>     validation=tb.conditions.RequiredConditionV1()
        >>> )
        ...
    """

    options: base_component_or(List[base_component_or(GroupFieldOption)], 'ListBaseComponentOrGroupFieldOption')  # noqa: F821
    disabled: base_component_or(bool) = attribute(kw_only=True)


@inherit_docstrings
class SelectFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_SELECT):
    """Button for selecting from a drop-down list.

    Use this component when the list is long and only one option can be chosen.

    For short lists (2-4 items), it's better to use field.radio-group or field.button-radio-group, where all the
    options are visible at once.

    To allow selecting multiple options, use the field.checkbox-group component.
    Attributes:
        options: Options to choose from.
        placeholder: The text that will be displayed if none of the options is selected.
    """

    class Option(BaseTemplate):
        """Options to choose from.

        Attributes:
            label: The name of the option to display in the list.
            value: The value to write to the data in the data property.
        """

        label: base_component_or(Any)
        value: base_component_or(Any)

    options: base_component_or(List[base_component_or(Option)], 'ListBaseComponentOrOption')  # noqa: F821
    placeholder: base_component_or(Any) = attribute(kw_only=True)


@inherit_docstrings
class TextFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_TEXT):
    """A component that allows entering a single line of text.

    Attributes:
        disabled: If true, editing is not available.
        placeholder: A semi-transparent label that is shown in the box when it is empty.
    """

    disabled: base_component_or(bool) = attribute(kw_only=True)
    placeholder: base_component_or(Any) = attribute(kw_only=True)


@inherit_docstrings
class TextAnnotationFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_TEXT_ANNOTATION):
    """A component for text segmentation.

    Use it to select multiple words, individual words, or letters in the text and label them with values. You can create
    multiple categories to label parts of the text, like all nouns and adjectives.

    You can use plugin.field.text-annotation.hotkeys to assign keyboard shortcuts for selecting categories.

    Attributes:
        adjust: If the property value is set to words, only words can be selected in the text. If you don't use this
            property, any part of a line can be selected.
        content: The text where the Toloker has to select part of a line.
        disabled: This property blocks the component. If true, the component is unavailable to the Toloker. The
            default value is false.
        labels: A category.
    """

    class Label(BaseTemplate):
        """
        Attributes:
            label: Specify the category name in the label property.
            value: Specify the category value in the value property.
        """

        label: base_component_or(str)
        value: base_component_or(str)

    adjust: base_component_or(str) = attribute(kw_only=True)
    content: base_component_or(str) = attribute(kw_only=True)
    disabled: base_component_or(bool) = attribute(kw_only=True)
    labels: base_component_or(List[base_component_or(Label)], 'ListBaseComponentOrLabel') = attribute(kw_only=True)  # noqa: F821


@inherit_docstrings
class TextareaFieldV1(BaseFieldV1, spec_value=ComponentType.FIELD_TEXTAREA):
    """Box for entering multi-line text.

    Use in tasks that require an extended response. For single-line responses, use the field.text component.

    The size of the box does not automatically adjust to the length of the text. Tolokers can change the height by
    dragging the lower-right corner. To change the default size of the box, use the rows property.

    Note that formatting is not available in the text box.
    Attributes:
        disabled: If true, editing is not available.
        placeholder: A semi-transparent label that is shown when the box is empty. Use it to provide an example or a
            hint for the response.
        resizable: Changing the box size. When set to true (the default value), the Toloker can change the height. To
            prevent resizing, set the value to false.
        rows: The height of the text box in lines.
    """

    disabled: base_component_or(bool) = attribute(kw_only=True)
    placeholder: base_component_or(Any) = attribute(kw_only=True)
    resizable: base_component_or(bool) = attribute(kw_only=True)
    rows: base_component_or(float) = attribute(kw_only=True)
