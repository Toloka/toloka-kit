import datetime
from enum import Enum, unique, auto
from typing import Optional, TypeVar, Type, Union, List, get_type_hints, cast

import attr

from ._converter import structure, unstructure
from .assignment import Assignment
from .attachment import Attachment
from .message_thread import Folder
from .pool import Pool
from .project import Project
from .training import Training
from .user_restriction import UserRestriction
from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass

SortItemSelf = TypeVar('SortItemSelf', bound='BaseSortItem')
SortItemsSelf = TypeVar('SortItemsSelf', bound='BaseSortItems')


@unique
class SortOrder(Enum):
    ASCENDING = auto()
    DESCENDING = auto()


class BaseSortItem(BaseTolokaObject):

    def unstructure(self):
        if self.order == SortOrder.DESCENDING:
            return f'-{self.field.value}'
        return f'{self.field.value}'

    @classmethod
    def structure(cls: Type[SortItemSelf], value: Union[SortItemSelf, str]) -> SortItemSelf:
        if isinstance(value, cls):
            return value

        value = cast(str, value)
        if value.startswith('-'):
            return cls(structure(value[1:], cls.SortField), SortOrder.DESCENDING)  # type: ignore
        return cls(structure(value, cls.SortField), SortOrder.ASCENDING)  # type: ignore

    @staticmethod
    def _create_sort_field_enum(sort_fields: List[str]):
        namespace = {field.upper(): field for field in sort_fields}
        return unique(Enum('SortField', namespace))  # type: ignore

    @classmethod
    def for_fields(cls, sort_fields: List[str]):
        sort_field_enum = cls._create_sort_field_enum(sort_fields)
        namespace = {
            'SortField': sort_field_enum,
            'order': SortOrder.ASCENDING,
            '__annotations__': {
                'field': sort_field_enum,
                'order': SortOrder,
            },
        }

        subclass = BaseTolokaObjectMetaclass('SortItem', (cls,), namespace, kw_only=False)
        subclass.__module__ = __name__
        return subclass


class BaseSortItems(BaseTolokaObject):

    def unstructure(self):
        return ','.join(unstructure(item) for item in self.items)

    @classmethod
    def structure(cls, items):
        if isinstance(items, cls):
            return items
        return cls(items=items)

    @classmethod
    def for_fields(cls, name: str, sort_fields: List[str]):
        sort_item_class: Type = BaseSortItem.for_fields(sort_fields)

        def items_converter(items):
            if isinstance(items, sort_items_class):
                return items
            if isinstance(items, str):
                items = items.split(',')
            return [sort_item_class.structure(item) for item in items]

        namespace = {
            'SortItem': sort_item_class,
            '__annotations__': {'items': List[sort_item_class]},  # type: ignore
            'items': attr.attrib(converter=items_converter),
        }
        sort_items_class = BaseTolokaObjectMetaclass(name, (BaseSortItems,), namespace, kw_only=False)
        sort_items_class.__module__ = __name__
        return sort_items_class


class SearchRequestMetaclass(BaseTolokaObjectMetaclass):

    def __new__(mcs, name, bases, namespace, kw_only=False, **kwargs):
        compare_fields_class = namespace['CompareFields']
        annotations = namespace.setdefault('__annotations__', {})

        # For every comparable field creating a corresponding attribute
        for field_name, field_type in get_type_hints(compare_fields_class).items():
            for suffix in 'lt', 'lte', 'gt', 'gte':
                condition_field = f'{field_name}_{suffix}'
                namespace[condition_field] = None
                annotations[condition_field] = Optional[field_type]

        # Building class
        subclass = super().__new__(mcs, name, bases, namespace, kw_only=kw_only, **kwargs)
        subclass.__module__ = __name__
        return subclass


class ProjectSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime

    status: Project.ProjectStatus


ProjectSortItems = BaseSortItems.for_fields('ProjectSortItems', ['id', 'created', 'public_name', 'private_comment'])


class PoolSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime
        last_started: datetime.datetime

    status: Pool.Status
    project_id: str


PoolSortItems = BaseSortItems.for_fields('PoolSortItems', ['id', 'created', 'last_started'])


class TrainingSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime
        last_started: datetime.datetime

    status: Training.Status
    project_id: str


TrainingSortItems = BaseSortItems.for_fields('TrainingSortItems', ['id', 'created', 'last_started'])


class SkillSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime

    name: str


SkillSortItems = BaseSortItems.for_fields('SkillSortItems', ['id', 'created'])


class AssignmentSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime
        submitted: datetime.datetime

    status: Assignment.Status
    task_id: str
    task_suite_id: str
    pool_id: str
    user_id: str


AssignmentSortItems = BaseSortItems.for_fields('AssignmentSortItems', ['id', 'created', 'submitted'])


class AggregatedSolutionSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        task_id: str


AggregatedSolutionSortItems = BaseSortItems.for_fields('AggregatedSolutionSortItems', ['task_id'])


class TaskSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime
        overlap: int

    pool_id: str
    overlap: int


TaskSortItems = BaseSortItems.for_fields('TaskSortItems', ['id', 'created'])


class TaskSuiteSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime
        overlap: int

    task_id: str
    pool_id: str
    overlap: int


TaskSuiteSortItems = BaseSortItems.for_fields('TaskSuiteSortItems', ['id', 'created'])


class AttachmentSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime

    name: str
    type: Attachment.Type
    user_id: str
    assignment_id: str
    pool_id: str

    owner_id: str
    owner_company_id: str


AttachmentSortItems = BaseSortItems.for_fields('AttachmentSortItems', ['id', 'created'])


class UserSkillSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime
        modified: datetime.datetime

    name: str

    user_id: str
    skill_id: str


UserSkillSortItems = BaseSortItems.for_fields('UserSkillSortItems', ['id', 'created'])


class UserRestrictionSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime

    scope: UserRestriction.Scope
    user_id: str
    project_id: str
    pool_id: str


UserRestrictionSortItems = BaseSortItems.for_fields('UserRestrictionSortItems', ['id', 'created'])


class UserBonusSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime

    user_id: str
    private_comment: str


UserBonusSortItems = BaseSortItems.for_fields('UserBonusSortItems', ['id', 'created'])


class MessageThreadSearchRequest(metaclass=SearchRequestMetaclass):

    class CompareFields:
        id: str
        created: datetime.datetime

    folder: Folder
    folder_ne: Folder


MessageThreadSortItems = BaseSortItems.for_fields('MessageThreadSortItems', ['id', 'created'])
