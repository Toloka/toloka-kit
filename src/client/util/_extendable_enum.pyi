__all__ = [
    'extend_enum',
    'ExtendableStrEnumMetaclass',
    'ExtendableStrEnum',
]
from enum import (
    Enum,
    EnumMeta
)

def extend_enum(
    enumeration: Enum,
    name: str,
    value: str
): ...


class ExtendableStrEnumMetaclass(EnumMeta):
    ...


class ExtendableStrEnum(Enum):
    """An enumeration.
    """

    ...
