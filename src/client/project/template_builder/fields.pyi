from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base import (
    BaseComponent,
    BaseTemplate,
    ListDirection,
    ListSize,
    VersionedBaseComponent
)


class BaseFieldV1(VersionedBaseComponent):
    """Fields for entering data, such as a text field or drop-down list.

    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]

class ButtonRadioFieldV1(BaseFieldV1):
    """A component in the form of a button.

    The user makes a choice by clicking on it.

    The size of the button depends on the size of the label.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        hint: Hint text.
        validation: Validation based on condition.
        value_to_set: The value of the output data when the button is clicked.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        value_to_set: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    value_to_set: Optional[Any]

class GroupFieldOption(BaseTemplate):
    """Option.

    Attributes:
        hint: Additional information.
        label: The text on the object.
        value: Returned value.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        label: Optional[Any] = ...,
        value: Optional[Any] = ...,
        hint: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    label: Optional[Any]
    value: Optional[Any]
    hint: Optional[Any]

class ButtonRadioGroupFieldV1(BaseFieldV1):
    """A component with buttons that allow the user to choose between the specified values.

    The minimum number of elements is one. Any type of data can be returned.

    The size of the button is determined by the length of the text on it.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        hint: Hint text.
        options: Array of information about the buttons.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]]

class CheckboxFieldV1(BaseFieldV1):
    """Checkbox.

    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        disabled: Property that disables the component. If true, the component will not be unavailable.
        hint: Hint text.
        preserve_false: Property that specifies whether to return false values in the results. By default, if the
            component returns false, this result will not be added to the output. To add false to the results, specify
            "preserveFalse": true.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        preserve_false: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    disabled: Optional[Union[BaseComponent, bool]]
    preserve_false: Optional[Union[BaseComponent, bool]]

class CheckboxGroupFieldV1(BaseFieldV1):
    """A group of options for selecting one or more responses.

    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        disabled: If `true', the options are inactive.
        hint: Hint text.
        options: Options, where value is the key that the option controls, and label is the text near the option.
        preserve_false: Property that specifies whether to return false values in the results. By default, if the
            component returns false, this result will not be added to the output. To add false to the results, specify
            "preserveFalse": true.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        preserve_false: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]]
    disabled: Optional[Union[BaseComponent, bool]]
    preserve_false: Optional[Union[BaseComponent, bool]]

class DateFieldV1(BaseFieldV1):
    """A component for entering the date and time in the desired format and range.

    You can set a list of dates that the user cannot select.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        block_list: List of dates that the user cannot select.
            * block_list[]: Date that the user cannot select.
        format: Format of the date entered by the user:
            * date-time — date and time.
            * date — date only.
        hint: Hint text.
        max: The latest date and time in the YYYY-MM-DD hh:mm format that the user can select. Where:
            * YYYY is the year.
            * MM is the month.
            * DD is the day.
            * hh is the time in hours.
            * mm is the time in minutes.
        min: The earliest date and time in the YYYY-MM-DD hh:mm format that the user can select. Where:
            * YYYY is the year.
            * MM is the month.
            * DD is the day.
            * hh is the time in hours.
            * mm is the time in minutes.
        placeholder: A semi-transparent label that is shown in the box when it is empty.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        format: Optional[Any] = ...,
        block_list: Optional[Union[BaseComponent, List[Any]]] = ...,
        max: Optional[Any] = ...,
        min: Optional[Any] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    format: Optional[Any]
    block_list: Optional[Union[BaseComponent, List[Any]]]
    max: Optional[Any]
    min: Optional[Any]
    placeholder: Optional[Any]

class EmailFieldV1(BaseFieldV1):
    """Creates a field for entering an email address.

    Checks that the text contains the @ character. You can set other conditions yourself.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        hint: Hint text.
        placeholder: A semi-transparent label that is shown in an empty field.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    placeholder: Optional[Any]

class FileFieldV1(BaseFieldV1):
    """This component can be used for uploading files. It's displayed in the interface as an upload button.

    You can restrict the file types to upload in the "accept" property. By default, only one file can be uploaded,
    but you can allow multiple files in the "multiple" property.

    If a user logs in from a mobile device, it's more convenient to use field.media-file — it's adapted for mobile
    devices and makes it easier to upload photos and videos.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        accept: A list of file types that can be uploaded. By default, you can upload any files.
            Specify the types in the format (https://developer.mozilla.org/en-US/docs/Web/HTTP/BasicsofHTTP/MIME_types).
            For example, you can allow only images to be uploaded by adding the image/jpeg and image/png types.
        hint: Hint text.
        multiple: Determines whether multiple files can be uploaded:
            * false (default) — forbidden.
            * true — allowed.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        accept: Optional[Union[BaseComponent, List[Union[BaseComponent, str]]]] = ...,
        multiple: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    accept: Optional[Union[BaseComponent, List[Union[BaseComponent, str]]]]
    multiple: Optional[Union[BaseComponent, bool]]

class ImageAnnotationFieldV1(BaseFieldV1):
    """Adds an interface for selecting areas in images.

    If you need to select different types of objects, classify the areas using the labels property.

    You can select areas using points, polygons, and rectangles. In the shapes property, you can keep some of the
    selection modes and hide the rest.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        disabled: Determines whether adding and deleting areas is allowed:
            * false (default) — Allowed.
            * true — Not allowed.
            You can use this feature when creating an interface to check whether the selection is correct,
             or if you need to allow selection only when a certain condition is met.
        full_height: If true, the element takes up all the vertical free space. The element is set to a minimum height
            of 400 pixels.
        hint: Hint text.
        image: The image you want to select areas in.
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
        validation: Validation based on condition.
    """

    class Label(BaseTemplate):
        """At least two objects must be added to the array.

        Attributes:
            label: Text on the button for selecting a selection color.
            value: The value to be written to the labels property data. Displayed to users as color options when
                selecting areas.
        """

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(
            self,*,
            label: Optional[Union[BaseComponent, str]] = ...,
            value: Optional[Union[BaseComponent, str]] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        label: Optional[Union[BaseComponent, str]]
        value: Optional[Union[BaseComponent, str]]

    class Shape(Enum):
        ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        full_height: Optional[Union[BaseComponent, bool]] = ...,
        image: Optional[Union[BaseComponent, str]] = ...,
        labels: Optional[Union[BaseComponent, List[Union[BaseComponent, Label]]]] = ...,
        min_width: Optional[Union[BaseComponent, float]] = ...,
        ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = ...,
        shapes: Optional[Union[BaseComponent, Dict[Union[BaseComponent, Shape], Union[BaseComponent, bool]]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    disabled: Optional[Union[BaseComponent, bool]]
    full_height: Optional[Union[BaseComponent, bool]]
    image: Optional[Union[BaseComponent, str]]
    labels: Optional[Union[BaseComponent, List[Union[BaseComponent, Label]]]]
    min_width: Optional[Union[BaseComponent, float]]
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]]
    shapes: Optional[Union[BaseComponent, Dict[Union[BaseComponent, Shape], Union[BaseComponent, bool]]]]

class ListFieldV1(BaseFieldV1):
    """A component that allows the user to add and remove list items, such as text fields to fill in.

    This way you can allow the user to give multiple answers to a question.

    The list items can contain any component, including a list of other components. For example, this allows you to
    create a table where you can add and delete rows.

    To add a new list item, the user clicks the button. To remove an item, they click on the x on the right (it appears
    when hovering over a list item).

    To prevent the user from adding too many list items, set the maximum list length. You can also use the editable
    property to block users from changing a component, like when a certain event occurs.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        button_label: Text on the button for adding list items.
        direction: The direction of the list.
        editable: A property that indicates whether adding and removing list items is allowed. Set false to disable.
            By default it is true (allowed).
        hint: Hint text.
        max_length: Maximum number of list items.
        render: Interface template for list items, such as a text field.
            In nested field.* components, use data.relative for recording responses, otherwise all the list items will
            have the same value.
        size: The distance between list items. Acceptable values in ascending order: s, m (default).
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        render: Optional[BaseComponent] = ...,
        button_label: Optional[Any] = ...,
        direction: Optional[Union[BaseComponent, ListDirection]] = ...,
        editable: Optional[Any] = ...,
        max_length: Optional[Union[BaseComponent, float]] = ...,
        size: Optional[Union[BaseComponent, ListSize]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    render: Optional[BaseComponent]
    button_label: Optional[Any]
    direction: Optional[Union[BaseComponent, ListDirection]]
    editable: Optional[Any]
    max_length: Optional[Union[BaseComponent, float]]
    size: Optional[Union[BaseComponent, ListSize]]

class MediaFileFieldV1(BaseFieldV1):
    """Adds buttons for different types of uploads: uploading photos or videos, selecting files from the file manager or choosing from the gallery. In the accept property, select which buttons you need.

    By default, only one file can be uploaded, but you can allow multiple files in the multiple property.

    This component is convenient when using mobile devices. To upload files from a computer, it's better to use
    field.file for a more flexible configuration of the file types.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        accept: Adds different buttons for four types of uploads. Pass the true value for the ones that you need.
            For example, if you need a button for uploading files from the gallery, add the "gallery": true property
        hint: Hint text.
        multiple: Determines whether multiple files can be uploaded:
        validation: Validation based on condition.
    """

    class Accept(BaseTemplate):
        """Adds different buttons for four types of uploads.

        Attributes:
            file_system: Adds a button for uploading files from the file manager.
            gallery: Adds a button for uploading files from the gallery.
            photo: Adds a button for uploading images.
            video: Adds a button for uploading videos.
        """

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(
            self,*,
            file_system: Optional[Union[BaseComponent, bool]] = ...,
            gallery: Optional[Union[BaseComponent, bool]] = ...,
            photo: Optional[Union[BaseComponent, bool]] = ...,
            video: Optional[Union[BaseComponent, bool]] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        file_system: Optional[Union[BaseComponent, bool]]
        gallery: Optional[Union[BaseComponent, bool]]
        photo: Optional[Union[BaseComponent, bool]]
        video: Optional[Union[BaseComponent, bool]]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        accept: Optional[Union[BaseComponent, Accept]] = ...,
        multiple: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    accept: Optional[Union[BaseComponent, Accept]]
    multiple: Optional[Union[BaseComponent, bool]]

class NumberFieldV1(BaseFieldV1):
    """A component that allows you to enter a number.

    The box already has validation: by default, users can enter only numbers and decimal separators. They can use either
    a dot or a comma as a separator, but there will always be a dot in the output.

    When the user is entering a number, the separator automatically changes to the one specified in the regional
    settings. For Russia, the separator is a comma.

    Negative numbers are allowed by default. To disable them, use the validation property. Pressing the up or down arrow
    keys will increase or decrease the number by one.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        hint: Hint text.
        maximum: Maximum number that can be entered.
        minimum: Minimum number that can be entered.
        placeholder: A semi-transparent label that is shown in the box when it is empty.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        maximum: Optional[Union[BaseComponent, int]] = ...,
        minimum: Optional[Union[BaseComponent, int]] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    maximum: Optional[Union[BaseComponent, int]]
    minimum: Optional[Union[BaseComponent, int]]
    placeholder: Optional[Any]

class PhoneNumberFieldV1(BaseFieldV1):
    """Creates a field for entering a phone number.

    Allows entering numbers, spaces, and the +, ( ), - characters. Only numbers and the + character at the beginning
    will remain in the data. For example, if you enter +7 (012) 345-67-89, the data gets the +70123456789 value.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        hint: Hint text.
        placeholder: A semi-transparent label that is shown in an empty field.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        placeholder: Optional[Union[BaseComponent, str]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    placeholder: Optional[Union[BaseComponent, str]]

class RadioGroupFieldV1(BaseFieldV1):
    """A component for selecting one value out of several options. It is designed as a group of circles arranged vertically.

    If you want it to look like normal buttons, use field.button-radio-group.

    The minimum number of buttons is one. Any type of data can be returned.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        disabled: This property prevents clicking the button. If the value is true, the button is not active (the user
            will not be able to click it).
        hint: Hint text.
        options: List of options to choose from
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]]
    disabled: Optional[Union[BaseComponent, bool]]

class SelectFieldV1(BaseFieldV1):
    """Button for selecting from a drop-down list.

    Use this component when the list is long and only one option can be chosen.

    For short lists (2-4 items), it's better to use field.radio-group or field.button-radio-group, where all the
    options are visible at once.

    To allow selecting multiple options, use the field.checkbox-group component.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        hint: Hint text.
        options: Options to choose from.
        placeholder: The text that will be displayed if none of the options is selected.
        validation: Validation based on condition.
    """

    class Option(BaseTemplate):
        """Options to choose from.

        Attributes:
            label: The name of the option to display in the list.
            value: The value to write to the data in the data property.
        """

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(
            self,*,
            label: Optional[Any] = ...,
            value: Optional[Any] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        label: Optional[Any]
        value: Optional[Any]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        options: Optional[Union[BaseComponent, Option]] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    options: Optional[Union[BaseComponent, Option]]
    placeholder: Optional[Any]

class TextFieldV1(BaseFieldV1):
    """A component that allows entering a single line of text.

    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        disabled: If true, editing is not available.
        hint: Hint text.
        placeholder: A semi-transparent label that is shown in the box when it is empty.
        validation: Validation based on condition.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    disabled: Optional[Union[BaseComponent, bool]]
    placeholder: Optional[Any]

class TextareaFieldV1(BaseFieldV1):
    """Box for entering multi-line text.

    Use in tasks that require an extended response. For single-line responses, use the field.text component.

    The size of the box does not automatically adjust to the length of the text. Users can change the height by
    dragging the lower-right corner. To change the default size of the box, use the rows property.

    Note that formatting is not available in the text box.
    Attributes:
        data: Data with values that will be processed or changed.
        label: Label above the component.
        disabled: If true, editing is not available.
        hint: Hint text.
        placeholder: A semi-transparent label that is shown when the box is empty. Use it to provide an example or a
            hint for the response.
        resizable: Changing the box size. When set to true (the default value), the user can change the height. To
            prevent resizing, set the value to false.
        rows: The height of the text box in lines.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        placeholder: Optional[Any] = ...,
        resizable: Optional[Union[BaseComponent, bool]] = ...,
        rows: Optional[Union[BaseComponent, float]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    disabled: Optional[Union[BaseComponent, bool]]
    placeholder: Optional[Any]
    resizable: Optional[Union[BaseComponent, bool]]
    rows: Optional[Union[BaseComponent, float]]
