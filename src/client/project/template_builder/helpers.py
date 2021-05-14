__all__ = [
    'BaseHelperV1',
    'ConcatArraysHelperV1',
    'Entries2ObjectHelperV1',
    'IfHelperV1',
    'JoinHelperV1',
    'Object2EntriesHelperV1',
    'ReplaceHelperV1',
    'SearchQueryHelperV1',
    'SwitchHelperV1',
    'TextTransformHelperV1',
    'TransformHelperV1',
    'YandexDiskProxyHelperV1'
]
from enum import Enum, unique
from typing import List, Any

from ...primitives.base import attribute

from .base import BaseComponent, ComponentType, BaseTemplate, VersionedBaseComponent, base_component_or


class BaseHelperV1(VersionedBaseComponent):
    """Perform various operations, such as if-then-else or switch-case.

    """

    pass


class ConcatArraysHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_CONCAT_ARRAYS):
    """Merging multiple arrays into a single array.

    For example, let's say you have multiple arrays:
    ([1, 2, 3], [4, 5, 6], [7, 8, 9])
    Their elements can be combined into a single array to show simultaneously:
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    Attributes:
        items: Arrays to combine.
    """

    items: base_component_or(List[base_component_or(Any)], 'ListBaseComponentOrAny')


class Entries2ObjectHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_ENTRIES2OBJECT):
    """Creating an object from a specified array of key-value pairs.

    For example, let's say you have an array like this:
    [
        {
            "key": "foo",
            "value": "hello"
        },
        {
            "key": "bar",
            "value": "world"
        }
    ]
    It is converted to an object whose elements consist of the values of the original array:
    { "foo": "hello", "bar": "world" }
    Attributes:
        entries: Source array of key-value pairs.
    """

    class Entry(BaseTemplate):
        key: base_component_or(str)
        value: base_component_or(Any)

    entries: base_component_or(List[base_component_or(Entry)], 'ListBaseComponentOrEntry')


class IfHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_IF):
    """The If...Then...Else operator.

    Allows you to execute either one block of code or another, depending on the condition. If you need more options,
    use helper.switch.

    For example, if you want to conduct a survey, you can use the helper.if component to ask the gender of the
    respondent and add different sets of questions, depending on whether the respondent is male or female.
    How it works: If the condition in if is true (returns true), the code specified in the then property will be
    executed. Otherwise (the condition is false and returns false) the code specified in else will be executed.
    The else property is optional. For example, let's say you ask the user " did you Like the image". You can make a
    comment field appear when a negative response is received, but nothing happens when a positive response is received.
    Attributes:
        condition: Condition to check.
        else_: The element that is returned if the condition from the condition property is false (returns false).
        then: The element that is returned if the condition from the condition property is true (returns true).

    Example:
        How to show a part of the interface by condition.

        >>> hidden_ui = tb.helpers.IfHelperV1(
        >>>     condition=tb.conditions.EqualsConditionV1(data=tb.data.OutputData(path='show_me'), to='show'),
        >>>     then=tb.view.ListViewV1(items=[header, buttons, images]),
        >>> )
        ...
    """

    condition: BaseComponent
    then: base_component_or(Any)
    else_: base_component_or(Any) = attribute(origin='else')


class JoinHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_JOIN):
    """The component combines two or more strings into one.

    You can add a delimiter to separate the strings, such as a space or comma.
    Attributes:
        by: Delimiter for joining strings. You can use any number of characters in the delimiter.
        items: Array of strings to join.
    """

    items: base_component_or(List[base_component_or(str)], 'ListBaseComponentOrStr')
    by: base_component_or(Any)


class Object2EntriesHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_OBJECT2ENTRIES):
    """Creating an array of key-value pairs from the specified object.

    For example, let's say you have an object that looks like this:
    {
        "foo": "hello",
        "bar": "world"
    }
    It will be converted to an array whose objects will pair data from the source object and their designations:
    [
        {
            "key": "foo",
            "value": "hello"
        },
        {
            "key": "bar",
            "value": "world"
        }
    ]
    Attributes:
        data: The object to convert.
    """

    data: base_component_or(Any)


class ReplaceHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_REPLACE):
    """Allows you to replace some parts of the string with others.

    This helper function returns a string in which all occurrences of 'findindataare replaced withreplace`.
    Because the helper.replace helper returns a string, it can be used in properties that accept string values.
    Attributes:
        data: Data to perform the replacement on.
        find: The value to search for — the string whose occurrences must be found in data and replaced with the string
            from replace.
        replace: The value to insert in place of the matches of the find value.
    """

    data: base_component_or(Any)
    find: base_component_or(str)
    replace: base_component_or(str)


class SearchQueryHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_SEARCH_QUERY):
    """Component for creating a string with a search query reference.

    The list of available search engines is specified in the engine enum.
    Attributes:
        engine: Search engine.
        query: Search query.
    """

    @unique
    class Engine(Enum):
        YANDEX = 'yandex'
        GOOGLE = 'google'
        BING = 'bing'
        MAILRU = 'mail.ru'
        WIKIPEDIA = 'wikipedia'
        YANDEX_COLLECTIONS = 'yandex/collections'
        YANDEX_VIDEO = 'yandex/video'
        YANDEX_IMAGES = 'yandex/images'
        GOOGLE_IMAGES = 'google/images'
        YANDEX_NEWS = 'yandex/news'
        GOOGLE_NEWS = 'google/news'

    query: base_component_or(Any)
    engine: base_component_or(Engine)


class SwitchHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_SWITCH):
    """A switch-case construction.

    Checks various conditions sequentially and executes the code from the result property when the corresponding
    condition is true.

    You can use it to perform an action or display an additional interface element only when a certain condition is met.
    View example in the sandbox.

    This helper is similar to a series of If...Then...Else logical expressions, so it is useful if there are more than
    two conditions for sequential verification. If you need to check one or two conditions, use the helper.if component.
    How the helper works:
        * The helper checks (conditions) from the array of cases objects, starting from the first one.
        * If the condition is true (returns true), the helper returns the result (block of code) specified in the result
          property for the condition object in the cases array. The helper quits and subsequent conditions are not
          checked.
        * If the condition is false (returns false), the helper checks the subsequent condition.
        * If all conditions are false as a result of all checks, the helper returns the value specified in the default
          property (if it is not defined, the helper returns nothing).
    Attributes:
        cases: An array of objects consisting of condition and result property pairs.
        default: Element that is returned if none of the checked conditions returned true.
    """

    class Case(BaseTemplate):
        """Case.

        Attributes:
            condition: Condition to check.
            result: The element that is returned if the condition from the condition property is true (returns true).
        """

        condition: BaseComponent
        result: base_component_or(Any)

    cases: base_component_or(List[base_component_or(Case)], 'ListBaseComponentOrCase')
    default: base_component_or(Any)


class TextTransformHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_TEXT_TRANSFORM):
    """Allows you to change the case of the text, like make all letters uppercase.

    For example, you can use this component to automatically process input data.

    This component is available in property values with the string type, for example in the content property in the
    view.text component.
    Attributes:
        data: The text string in which you want to change the case.
        transformation: Conversion mode.
    """

    @unique
    class Transformation(Enum):
        UPPERCASE = 'uppercase'
        LOWERCASE = 'lowercase'
        CAPITALIZE = 'capitalize'

    data: base_component_or(Any)
    transformation: base_component_or(Transformation)


class TransformHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_TRANSFORM):
    """Creates a new array by transforming each of the elements in the original array.

    For example, you can convert an array of image links to view.image components to display these images. This may be
    useful if the number of images in the array is unknown in advance
    Attributes:
        into: Template to transform elements in the array. The array value can be substituted using the data.local
            component. To do this, use the construction { "type": "data.local", "path": "item"}
        items: The array that you want to convert. You can specify an array in three ways:
            * Specify the array itself. Example: ["one", "two", "three"].
            * Insert a reference to data (input, output, or internal). Example: {"type": "data.input",
                "path": "path.to.data"}.
            * Use a reference to another configuration element. Example: {"$ref": "vars.myarray"}.
    """

    into: base_component_or(Any)
    items: base_component_or(List[base_component_or(Any)], 'ListBaseComponentOrAny')


class YandexDiskProxyHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_YANDEX_DISK_PROXY):
    """You can use this component to download files from Yandex.Disk.

    To use YandexDiskProxyHelper, connect Yandex.Disk to your Toloka account and add the proxy by following
    the instructions: https://yandex.com/support/toloka-requester/concepts/prepare-data.html?lang=en
    Select the component that you want to add, such as view.image for an image or view.audio for an audio file.
    In the url property of this component, use YandexDiskProxyHelper.
    Attributes:
        path: Path to the file in the /&lt;Proxy name&gt;/&lt;File name&gt;.&lt;type&gt; format
    """

    path: base_component_or(str)
