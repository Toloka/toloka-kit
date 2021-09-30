__all__ = [
    'extend_enum',
    'ExtendableStrEnumMetaclass',
    'ExtendableStrEnum',
]
import enum


def extend_enum(
    enumeration: enum.Enum,
    name: str,
    value: str
): ...


class ExtendableStrEnumMetaclass(enum.EnumMeta):
    ...


class ExtendableStrEnum(enum.Enum):
    """An enumeration.
    """

    ...
