__all__ = [
    'VariantRegistry',
    'attribute',
    'BaseTolokaObjectMetaclass',
    'BaseTolokaObject'
]
from copy import copy
from enum import Enum
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar, Union

import attr

from .._converter import converter
from ..exceptions import SpecClassIdentificationError

REQUIRED_KEY = 'toloka_field_required'
ORIGIN_KEY = 'toloka_field_origin'

E = TypeVar('E', bound=Enum)


class VariantRegistry:

    def __init__(self, field: str, enum: Type[E]):
        self.field: str = field
        self.enum: Type[E] = enum
        self.registered_classes: Dict[E, type] = {}

    def register(self, type_: type, value: E) -> type:

        if not isinstance(value, self.enum):
            raise TypeError(f'spec_value must be an instance of {self.enum} not {value}')

        if value in self.registered_classes:
            raise TypeError(f'Specification for {value} is already registered')

        setattr(type_, self.field, value)
        self.registered_classes[value] = type_

        return type_

    def __getitem__(self, value: E):
        return self.registered_classes[value]


def attribute(*args, required=False, origin=None, **kwargs):
    metadata = {}
    if required:
        metadata[REQUIRED_KEY] = True
    if origin:
        metadata[ORIGIN_KEY] = origin

    return attr.attrib(*args, metadata=metadata, **kwargs)


class BaseTolokaObjectMetaclass(type):

    def __new__(mcs, name, bases, namespace, auto_attribs=True, kw_only=True, frozen=False, order=True, eq=True, **kwargs):
        cls = attr.attrs(
            auto_attribs=auto_attribs,
            kw_only=kw_only,
            field_transformer=mcs.transformer,
            frozen=frozen,
            order=order,
            eq=eq,
            str=True,
            collect_by_mro=True,
        )(super().__new__(mcs, name, bases, namespace, **kwargs))

        # Transformer's change in field type does not affect created
        # class's annotations. So we synchronize them manually
        annotations = getattr(cls.__dict__, '__annotations__', {})
        for field in attr.fields(cls):
            if field.type is not None:
                annotations[field.name] = field.type
        cls.__annotations__ = annotations

        return cls

    @staticmethod
    def transformer(type_: type, fields: List[attr.Attribute]) -> List[attr.Attribute]:
        transformed_fields = []

        for field in fields:
            # Make all attributes optional unless explicitly configured otherwise
            if not field.metadata.get(REQUIRED_KEY):
                field = field.evolve(
                    type=Optional[field.type] if field.type else field.type,
                    default=None if field.default is attr.NOTHING else field.default,
                )

            transformed_fields.append(field)

        return transformed_fields


class BaseTolokaObject(metaclass=BaseTolokaObjectMetaclass):
    """
    A base class for classes representing Toloka objects.



    Subclasses of BaseTolokaObject will:
    * Automatically convert annotated attributes attributes via attrs making them optional
      if not explicitly configured otherwise
    * Skip missing optional fields during unstructuring with client's cattr converter
    """

    _variant_registry: ClassVar[Optional[VariantRegistry]] = None
    _unexpected: Dict[str, Any] = attribute(factory=dict, init=False)

    def __new__(cls, *args, **kwargs):
        """Overriding new for our check to be executed before auto-generated __init__"""
        if cls.is_variant_incomplete():
            message = 'Cannot instantiate an incomplete variant type on field {}'
            raise TypeError(message.format(cls._variant_registry.field))

        return super().__new__(cls)

    @classmethod
    def __init_subclass__(cls, spec_enum: Optional[Union[str, Type[E]]] = None,
                          spec_field: Optional[str] = None, spec_value=None):

        # Completing a variant type
        if spec_value is not None:
            cls._variant_registry.register(cls, spec_value)

        # Making into a variant type
        if spec_enum is not None or spec_field is not None:

            if spec_enum is None or spec_field is None:
                raise ValueError('Both spec_enum and spec_field must be provided')

            if cls.is_variant_incomplete():
                message = 'Incomplete variant type on field {} cannot be a variant type itself'
                raise TypeError(message.format(cls._variant_registry.field))

            # TODO: Possibly make it immutable
            enum = getattr(cls, spec_enum) if isinstance(spec_enum, str) else spec_enum
            cls._variant_registry = VariantRegistry(spec_field, enum)

    # Unexpected fields access

    def __getattr__(self, item):
        try:
            return self._unexpected[item]
        except KeyError as exc:
            raise AttributeError(str(item)) from exc

    # Variant type related checks

    @classmethod
    def is_variant_base(cls) -> bool:
        return '_variant_registry' in cls.__dict__

    @classmethod
    def is_variant_incomplete(cls) -> bool:
        return cls._variant_registry and cls._variant_registry.field not in cls.__dict__  # type: ignore

    @classmethod
    def is_variant_spec(cls) -> bool:
        return cls._variant_registry and cls._variant_registry.field in cls.__dict__  # type: ignore

    @classmethod
    def get_variant_specs(cls) -> dict:
        variant_specs = {}
        for base in cls.__mro__:
            registry = base.__dict__.get('_variant_registry')
            if registry:
                variant_specs[registry.field] = getattr(cls, registry.field)

        return variant_specs

    @classmethod
    def get_spec_subclass_for_value(cls, spec_value: Union[str, E] = None) -> type:
        try:
            spec_value = cls._variant_registry.enum(spec_value)
        except ValueError:
            return None
        return cls._variant_registry[spec_value]

    # Conversions related functions

    def unstructure(self) -> Optional[dict]:
        data = dict(self._unexpected)
        obj_class = type(self)

        for field in attr.fields(obj_class):
            if field.name == '_unexpected':
                continue

            value = converter.unstructure(getattr(self, field.name))
            if field.metadata.get(REQUIRED_KEY) or value is not None:
                key = field.metadata.get(ORIGIN_KEY, field.name)
                data[key] = value

        data.update(converter.unstructure(self.get_variant_specs()))
        assert '_unexpected' not in data
        return data or None

    @classmethod
    def structure(cls, data: dict):

        # If a class is an incomplete variant type we structure it into
        # one of its subclasses
        if cls.is_variant_incomplete():
            # TODO: Optimize copying
            data = dict(data)  # Do not modify input data
            spec_field = cls._variant_registry.field
            data_field = data.pop(spec_field)
            try:
                spec_value = cls._variant_registry.enum(data_field)
                spec_class = cls._variant_registry.registered_classes[spec_value]
            except Exception:
                raise SpecClassIdentificationError(spec_field=spec_field,
                                                   spec_enum=cls._variant_registry.enum.__name__)
            return spec_class.structure(data)

        data = copy(data)
        kwargs = {}

        for field in attr.fields(cls):
            key = field.metadata.get(ORIGIN_KEY, field.name)
            if key not in data:
                continue

            value = data.pop(key)
            if field.type is not None:
                value = converter.structure(value, field.type)

            kwargs[field.name] = value

        obj = cls(**kwargs)
        obj._unexpected = data
        return obj
