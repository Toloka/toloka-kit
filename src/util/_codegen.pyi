__all__ = [
    'attribute',
    'fix_attrs_converters',
]
import typing


def attribute(
    *args,
    required: bool = False,
    origin: typing.Optional[str] = None,
    readonly: bool = False,
    autocast: bool = False,
    **kwargs
):
    """Proxy for attr.attrib(...). Adds several keywords.

    Args:
        *args: All positional arguments from attr.attrib
        required: If True makes attribute not Optional. All other attributes are optional by default. Defaults to False.
        origin: Sets field name in dict for attribute, when structuring/unstructuring from dict. Defaults to None.
        readonly: Affects only when the class 'expanding' as a parameter in some function. If True, drops this attribute from expanded parameters. Defaults to None.
        autocast: If True then converter.structure will be used to convert input value
        **kwargs: All keyword arguments from attr.attrib
    """
    ...


def fix_attrs_converters(cls):
    """Due to https://github.com/Toloka/toloka-kit/issues/37 we have to support attrs>=20.3.0.
    This version lacks a feature that uses converters' annotations in class's __init__
    (see https://github.com/python-attrs/attrs/pull/710)). This decorator brings this feature
    to older attrs versions.
    """
    ...
