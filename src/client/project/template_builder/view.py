__all__ = [
    'BaseViewV1',
    'ActionButtonViewV1',
    'AlertViewV1',
    'AudioViewV1',
    'CollapseViewV1',
    'DeviceFrameViewV1',
    'DividerViewV1',
    'GroupViewV1',
    'IframeViewV1',
    'ImageViewV1',
    'LabeledListViewV1',
    'LinkViewV1',
    'LinkGroupViewV1',
    'ListViewV1',
    'MarkdownViewV1',
    'TextViewV1',
    'VideoViewV1'
]
from enum import unique
from typing import List, Any

from .base import (
    BaseTemplate,
    BaseComponent,
    ListDirection,
    ListSize,
    ComponentType,
    VersionedBaseComponentMetaclass,
    base_component_or
)
from ....util._codegen import attribute
from ....util._extendable_enum import ExtendableStrEnum


class BaseViewV1Metaclass(VersionedBaseComponentMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):

        if 'hint' not in namespace:
            namespace['hint'] = attribute(kw_only=True)
            namespace.setdefault('__annotations__', {})['hint'] = base_component_or(Any)
        if 'label' not in namespace:
            namespace['label'] = attribute(kw_only=True)
            namespace.setdefault('__annotations__', {})['label'] = base_component_or(Any)
        if 'validation' not in namespace:
            namespace['validation'] = attribute(kw_only=True)
            namespace.setdefault('__annotations__', {})['validation'] = BaseComponent
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class BaseViewV1(BaseComponent, metaclass=BaseViewV1Metaclass):
    """Elements displayed in the interface, such as text, list, audio player, or image.

    """

    pass


class ActionButtonViewV1(BaseViewV1, spec_value=ComponentType.VIEW_ACTION_BUTTON):
    """Button that calls an action.

    When clicking the button, an action specified in the action property is called.
    Attributes:
        action: Action called when clicking the button.
        label: Button text.
        hint: Hint text.
        validation: Validation based on condition.
    """

    action: BaseComponent


class AlertViewV1(BaseViewV1, spec_value=ComponentType.VIEW_ALERT):
    """The component creates a color block to highlight important information.

    You can use both plain text and other visual components inside it.
    Attributes:
        content: Content of the block with important information.
        label: Label above the component.
        hint: Hint text.
        theme: Determines the block color.
        validation: Validation based on condition.
    """

    @unique
    class Theme(ExtendableStrEnum):
        """An enumeration

        Attributes:
            INFO: (default) Blue.
            SUCCESS: Green.
            WARNING: Yellow.
            DANGER: Red.
        """

        DANGER = 'danger'
        INFO = 'info'
        SUCCESS = 'success'
        WARNING = 'warning'

    content: BaseComponent
    theme: base_component_or(Theme) = attribute(kw_only=True)


class AudioViewV1(BaseViewV1, spec_value=ComponentType.VIEW_AUDIO):
    """The component plays audio.

    Format support depends on the user's browser, OS, and device. We recommend using MP3.
    Attributes:
        url: Audio link.
        label: Label above the component.
        hint: Hint text.
        loop: Automatically replay audio.
        validation: Validation based on condition.
    """

    url: base_component_or(Any)
    loop: base_component_or(bool) = attribute(kw_only=True)


class CollapseViewV1(BaseViewV1, spec_value=ComponentType.VIEW_COLLAPSE):
    """Expandable block.

    Lets you add hidden content that doesn't need to be shown initially or that takes up a large space.

    The block heading is always visible.

    If you set the defaultOpened property to true, the block is expanded immediately, but it can be collapsed.
    Attributes:
        label: Block heading.
        content: Content hidden in the block.
        default_opened: If true, the block is immediately displayed in expanded form. By default, false (the block is
            collapsed).
        hint: Hint text.
        validation: Validation based on condition.
    """

    label: base_component_or(Any)
    content: BaseComponent
    default_opened: base_component_or(bool) = attribute(origin='defaultOpened', kw_only=True)


class DeviceFrameViewV1(BaseViewV1, spec_value=ComponentType.VIEW_DEVICE_FRAME):
    """Wraps the content of a component in a frame that is similar to a mobile phone.

    You can place other components inside the frame.
    Attributes:
        content: Content inside the frame.
        label: Label above the component.
        full_height: If true, the element takes up all the vertical free space. The element is set to a minimum height
            of 400 pixels.
        hint: Hint text.
        max_width: Maximum width of the element in pixels, must be greater than min_width.
        min_width: Minimum width of the element in pixels. Takes priority over max_width.
        ratio: An array of two numbers that sets the relative dimensions of the sides: width (first number) to
            height (second number). Not valid if full_height=true.
        validation: Validation based on condition.
    """

    content: BaseComponent
    full_height: base_component_or(bool) = attribute(origin='fullHeight', kw_only=True)
    max_width: base_component_or(float) = attribute(origin='maxWidth', kw_only=True)
    min_width: base_component_or(float) = attribute(origin='minWidth', kw_only=True)
    ratio: base_component_or(List[base_component_or(float)], 'ListBaseComponentOrFloat') = attribute(kw_only=True)


class DividerViewV1(BaseViewV1, spec_value=ComponentType.VIEW_DIVIDER):
    """Horizontal delimiter.

    You can place extra elements in the center of the delimiter, like a popup hint and label.
    Attributes:
        label: A label in the center of the delimiter. Line breaks are not supported.
        hint: Hint text.
        validation: Validation based on condition.
    """

    pass


class GroupViewV1(BaseViewV1, spec_value=ComponentType.VIEW_GROUP):
    """Groups components visually into framed blocks.

    Attributes:
        content: Content of a group block.
        label: Group heading.
        hint: Explanation of the group heading. To insert a new line, use
            .
        validation: Validation based on condition.
    """

    content: BaseComponent


class IframeViewV1(BaseViewV1, spec_value=ComponentType.VIEW_IFRAME):
    """Displays the web page at the URL in an iframe window.

    Attributes:
        url: URL of the web page.
        label: Label above the component.
        full_height: If true, the element takes up all the vertical free space. The element is set to a minimum height
            of 400 pixels.
        hint: Hint text.
        max_width: Maximum width of the element in pixels, must be greater than min_width.
        min_width: Minimum width of the element in pixels. Takes priority over max_width.
        ratio: An array of two numbers that sets the relative dimensions of the sides: width (first number) to
            height (second number). Not valid if full_height=true.
        validation: Validation based on condition.
    """

    url: base_component_or(str)
    full_height: base_component_or(bool) = attribute(origin='fullHeight', kw_only=True)
    max_width: base_component_or(float) = attribute(origin='maxWidth', kw_only=True)
    min_width: base_component_or(float) = attribute(origin='minWidth', kw_only=True)
    ratio: base_component_or(List[base_component_or(float)], 'ListBaseComponentOrFloat') = attribute(kw_only=True)


class ImageViewV1(BaseViewV1, spec_value=ComponentType.VIEW_IMAGE):
    """Displays an image.

    Attributes:
        url: Image link.
        label: Label above the component.
        full_height: If true, the element takes up all the vertical free space. The element is set to a minimum height
            of 400 pixels.
        hint: Hint text.
        max_width: Maximum width of the element in pixels, must be greater than min_width.
        min_width: Minimum width of the element in pixels. Takes priority over max_width.
        no_border: Controls the display of a frame around an image. By default, true (the frame is hidden). Set false
            to display the frame.
        no_lazy_load: Disables lazy loading. If true, images start loading immediately, even if they aren't in the
            viewport. Useful for icons. By default, false (lazy loading is enabled). In this mode, images start loading
            only when they get in the user's field of view.
        popup: Specifies whether opening a full-size image with a click is allowed. By default, it is true (allowed).
        ratio: An array of two numbers that sets the relative dimensions of the sides: width (first number) to
            height (second number). Not valid if full_height=true.
        scrollable: When set to true, an image has scroll bars if it doesn't fit in the parent element.
            If false, the image fits in the parent element and, when clicked, opens in its original size in the module
            window.
            Images in SVG format with no size specified always fit in their parent elements.
        validation: Validation based on condition.
    """

    url: base_component_or(Any)
    full_height: base_component_or(bool) = attribute(origin='fullHeight', kw_only=True)
    max_width: base_component_or(float) = attribute(origin='maxWidth', kw_only=True)
    min_width: base_component_or(float) = attribute(origin='minWidth', kw_only=True)
    no_border: base_component_or(bool) = attribute(origin='noBorder', kw_only=True)
    no_lazy_load: base_component_or(bool) = attribute(origin='noLazyLoad', kw_only=True)
    popup: base_component_or(bool) = attribute(kw_only=True)
    ratio: base_component_or(List[base_component_or(float)], 'ListBaseComponentOrFloat') = attribute(kw_only=True)
    rotatable: base_component_or(bool) = attribute(kw_only=True)
    scrollable: base_component_or(bool) = attribute(kw_only=True)


class LabeledListViewV1(BaseViewV1, spec_value=ComponentType.VIEW_LABELED_LIST):
    """Displaying components as a list with labels placed on the left.

    If you don't need labels, use view.list.
    Attributes:
        items: List items.
        label: Label above the component.
        hint: Hint text.
        min_width: The minimum width of list content. If the component width is less than the specified value, it
            switches to compact mode.
        validation: Validation based on condition.
    """

    class Item(BaseTemplate):
        """Item.

        Attributes:
            content: List item content.
            label: A label displayed next to a list item.
            center_label: If true, a label is center-aligned relative to the content of a list item (content). Use it
                if the list consists of large items, such as images or multi-line text.
                By default, false (the label is aligned to the top of the content block).
            hint: A pop-up hint displayed next to a label.
        """

        content: BaseComponent
        label: base_component_or(Any)
        center_label: base_component_or(bool) = attribute(origin='centerLabel', kw_only=True)
        hint: base_component_or(Any) = attribute(kw_only=True)

    items: base_component_or(List[base_component_or(Item)], 'ListBaseComponentOrItem')
    min_width: base_component_or(float) = attribute(origin='minWidth', kw_only=True)


class LinkViewV1(BaseViewV1, spec_value=ComponentType.VIEW_LINK):
    """Universal way to add a link.

    This link changes color when clicked.

    We recommend using this component if you need to insert a link without additional formatting.

    If you want to insert a button that will open the link, use the view.action-button and action.open-link components.

    To insert a link with a search query, use helper.search-query.
    Attributes:
        url: Link URL.
        label: Label above the component.
        content: Link text displayed to the user.
        hint: Hint text.
        validation: Validation based on condition.
    """

    url: base_component_or(Any)
    content: base_component_or(Any) = attribute(kw_only=True)


class LinkGroupViewV1(BaseViewV1, spec_value=ComponentType.VIEW_LINK_GROUP):
    """Puts links into groups

    The most important link in a group can be highlighted with a border: set the theme property to primary for this link.
    This only groups links, unlike GroupViewV1.

    Attributes:
        links: Array of links that make up a group.
        label: Label above the component.
        hint: Hint text.
        validation: Validation based on condition.

    Example:
        How to add several links.

        >>> links = tb.view.LinkGroupViewV1(
        >>>     [
        >>>         tb.view.LinkGroupViewV1.Link(
        >>>             'https://any.com/useful/url/1',
        >>>             'Example1',
        >>>         ),
        >>>         tb.view.LinkGroupViewV1.Link(
        >>>             'https://any.com/useful/url/2',
        >>>             'Example2',
        >>>         ),
        >>>     ]
        >>> )
        ...
    """

    class Link(BaseTemplate):
        """Link parameters

        Attributes:
            url: Link address
            content: Link text that's displayed to the user. Unviewed links are blue and underlined, and clicked links are purple.
            theme: Defines the appearance of the link. If you specify "theme": "primary", it's a button, otherwise it's a text link.
        """

        url: base_component_or(str)
        content: base_component_or(str)
        theme: base_component_or(str) = attribute(kw_only=True)

    links: base_component_or(List[base_component_or(Link)], 'ListBaseComponentOrLink')


class ListViewV1(BaseViewV1, spec_value=ComponentType.VIEW_LIST):
    """Block for displaying data in a list.

    Attributes:
        items:  Array of list items.
        label: Label above the component.
        direction: Determines the direction of the list.
        hint: Hint text.
        size: Specifies the size of the margins between elements. Acceptable values in ascending order: s, m (default
            value).
        validation: Validation based on condition.
    """

    items: base_component_or(List[BaseComponent], 'ListBaseComponent')
    direction: base_component_or(ListDirection) = attribute(kw_only=True)
    size: base_component_or(ListSize) = attribute(kw_only=True)


class MarkdownViewV1(BaseViewV1, spec_value=ComponentType.VIEW_MARKDOWN):
    """Block for displaying text in Markdown.

    The contents of the block are written to the content property in a single line. To insert line breaks, use \\n
    Straight quotation marks (") must be escaped like this: \\".

    Note that the view.markdown component is resource-intensive and might overload weak user devices.
    Do not use this component to display plain text. If you need to display text without formatting, use the view.text
    component. If you need to insert a link, use view.link, and for an image use view.image.
    Links with Markdown are appended with target="_blank" (the link opens in a new tab), as well as
    rel="noopener noreferrer"

    Attributes:
        content: Text in Markdown.
        label: Label above the component.
        hint: Hint text.
        validation: Validation based on condition.

    Example:
        How to add a title and description on the task interface.

        >>> header = tb.view.MarkdownViewV1('# Some Header:\n---\nSome detailed description')
        ...
    """

    content: base_component_or(Any)


class TextViewV1(BaseViewV1, spec_value=ComponentType.VIEW_TEXT):
    """Block for displaying text.

    If you need formatted text, use view.markdown.
    Attributes:
        content: The text displayed in the block. To insert a new line, use \n
        label: Label above the component.
        hint: Hint text.
        validation: Validation based on condition.

    Example:
        How to show labeled field from the task inputs.

        >>> text_view = tb.view.TextViewV1(tb.data.InputData('input_field_name'), label='My label:')
        ...
    """

    content: base_component_or(Any)


class VideoViewV1(BaseViewV1, spec_value=ComponentType.VIEW_VIDEO):
    """Player for video playback.

    The player is a rectangular block with a frame and buttons to control the video. You can set the block size using
    the ratio, fullHeight, minWidth, and maxWidth properties.

    The video resolution does not affect the size of the block — the video will fit into the block and will not be
    cropped.
    Attributes:
        url: Link to the video file.
        label: Label above the component.
        full_height: If true, the element takes up all the vertical free space. The element is set to a minimum height
            of 400 pixels.
        hint: Hint text.
        max_width: Maximum width of the element in pixels, must be greater than min_width.
        min_width: Minimum width of the element in pixels. Takes priority over max_width.
        ratio: The aspect ratio of the video block. An array of two numbers: the first sets the width of the block and
            the second sets the height.
        validation: Validation based on condition.
    """

    url: base_component_or(Any)
    full_height: base_component_or(bool) = attribute(origin='fullHeight', kw_only=True)
    max_width: base_component_or(float) = attribute(origin='maxWidth', kw_only=True)
    min_width: base_component_or(float) = attribute(origin='minWidth', kw_only=True)
