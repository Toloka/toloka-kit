from enum import Enum, unique
from typing import List, Any

from ...primitives.base import attribute

from .base import BaseComponent, ComponentType, BaseTemplate, VersionedBaseComponent, base_component_or


class BaseHelperV1(VersionedBaseComponent):
    pass


class ConcatArraysHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_CONCAT_ARRAYS):
    items: base_component_or(List[base_component_or(Any)], 'ListBaseComponentOrAny')


class Entries2ObjectHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_ENTRIES2OBJECT):

    class Entry(BaseTemplate):
        key: base_component_or(str)
        value: base_component_or(Any)

    entries: base_component_or(List[base_component_or(Entry)], 'ListBaseComponentOrEntry')


class IfHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_IF):
    condition: BaseComponent
    then: base_component_or(Any)
    else_: base_component_or(Any) = attribute(origin='else')


class JoinHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_JOIN):
    items: base_component_or(List[base_component_or(str)], 'ListBaseComponentOrStr')
    by: base_component_or(Any)


class Object2EntriesHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_OBJECT2ENTRIES):
    data: base_component_or(Any)


class ReplaceHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_REPLACE):
    data: base_component_or(Any)
    find: base_component_or(str)
    replace: base_component_or(str)


class SearchQueryHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_SEARCH_QUERY):

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

    class Case(BaseTemplate):
        condition: BaseComponent
        result: base_component_or(Any)

    cases: base_component_or(List[base_component_or(Case)], 'ListBaseComponentOrCase')
    default: base_component_or(Any)


class TextTransformHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_TEXT_TRANSFORM):

    @unique
    class Transformation(Enum):
        UPPERCASE = 'uppercase'
        LOWERCASE = 'lowercase'
        CAPITALIZE = 'capitalize'

    data: base_component_or(Any)
    transformation: base_component_or(Transformation)


class TransformHelperV1(BaseHelperV1, spec_value=ComponentType.HELPER_TRANSFORM):
    into: base_component_or(Any)
    items: base_component_or(List[base_component_or(Any)], 'ListBaseComponentOrAny')
