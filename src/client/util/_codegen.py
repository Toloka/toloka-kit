__all__: list = ['BaseParameters']
import functools
import linecache
import uuid
from inspect import signature, Signature, Parameter
from textwrap import dedent, indent
from typing import Callable

import attr

from ..primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass
from ..util._typing import is_optional_of


def _get_signature(func: Callable):
    """
    Correctly processes a signature for a callable. Correctly processes
    classes
    """
    if isinstance(func, type):
        sig = signature(func.__init__)  # type: ignore
        params = list(sig.parameters.values())
        return sig.replace(parameters=params[1:])
    return signature(func)


def _remove_annotations_from_signature(sig: Signature) -> Signature:
    """
    Returns a new Signature object that differs from the
    original one only by annotation
    """
    params = sig.parameters.values()
    new_params = [p.replace(annotation=Parameter.empty) for p in params]
    return Signature(parameters=new_params)


def _make_keyword_only_signature(sig: Signature) -> Signature:
    """
    Returns a new Signature object where all arguments are
    positional only
    """
    new_params = []
    for param in sig.parameters.values():
        if param.kind in (Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD):
            new_params.append(param)
        elif param.kind == Parameter.POSITIONAL_OR_KEYWORD:
            new_params.append(param.replace(kind=Parameter.KEYWORD_ONLY))
        else:
            raise ValueError(f'Cannot convert signature {sig} to keyword-only')

    return sig.replace(parameters=new_params)


def _get_annotations_from_signature(sig: Signature) -> dict:
    annotations = {
        p.name: p.annotation
        for p in sig.parameters.values()
        if p.annotation != Parameter.empty
    }

    if sig.return_annotation != Parameter.empty:
        annotations['return'] = sig.return_annotation

    return annotations


def _get_signature_invocation_string(sig: Signature) -> str:
    """
    Generates a string that could be added to a function
    with provided signature to initiate a completely valid
    call assuming that we have variables in our local scope
    named the same way as signature arguments
    """
    tokens = []

    for param in sig.parameters.values():
        if param.kind == Parameter.VAR_POSITIONAL:
            tokens.append(f'*{param.name}')
        elif param.kind == Parameter.VAR_KEYWORD:
            tokens.append(f'**{param.name}')
        elif param.kind == Parameter.KEYWORD_ONLY:
            tokens.append(f'{param.name}={param.name}')
        else:
            tokens.append(param.name)

    return '(' + ', '.join(tokens) + ')'


def _compile_function(func_name, func_sig, func_body, globs=None):
    file_name = f'{func_name}_{uuid.uuid4().hex}'
    annotations = _get_annotations_from_signature(func_sig)
    sig = _remove_annotations_from_signature(func_sig)

    source = f'def {func_name}{sig}:\n{indent(func_body, " " * 4)}'
    bytecode = compile(source, file_name, 'exec')
    namespace = {}
    eval(bytecode, {} if globs is None else globs, namespace)

    func = namespace[func_name]
    func.__annotations__ = annotations

    linecache.cache[file_name] = (
        len(source),
        None,
        source.splitlines(True),
        file_name
    )

    return func


def create_setter(attr_path: str, attr_type=Parameter.empty):
    """Generates a setter method for an attribute"""
    attr_name = attr_path.split('.')[-1]
    return _compile_function(
        f'codegen_setter_for_{attr_path.replace(".", "_")}',
        Signature(parameters=[
            Parameter(name='self', kind=Parameter.POSITIONAL_OR_KEYWORD),
            Parameter(name=attr_name, kind=Parameter.POSITIONAL_OR_KEYWORD, annotation=attr_type),
        ]),
        (
            f'"""A shortcut setter for {attr_path}"""\n'
            f'self.{attr_path} = {attr_name}'
        )
    )


def codegen_attr_attributes_setters(cls):
    """
    Adds setters for both required or optional attributes with attr
    constructed types. Resulting signatures are identical to the
    attribute type's constructor's.
    """
    for field in attr.fields(cls):
        type_ = is_optional_of(field.type) or field.type
        if attr.has(type_):
            setter_name = f'set_{field.name}'
            setter = expand(field.name)(create_setter(field.name, type_))
            setattr(cls, setter_name, setter)
    return cls


def expand_func_by_argument(func: Callable, arg_name: str) -> Callable:
    func_sig = _get_signature(func)
    func_params = list(func_sig.parameters.values())

    arg_param = func_sig.parameters[arg_name]
    arg_index = next(i for (i, p) in enumerate(func_params) if p is arg_param)
    arg_type = is_optional_of(arg_param.annotation) or arg_param.annotation
    arg_type_sig = _get_signature(arg_type)

    # TODO: add tests
    if arg_param.kind == Parameter.KEYWORD_ONLY:
        arg_type_sig = _make_keyword_only_signature(arg_type_sig)

    new_params = list(func_params)
    new_params[arg_index:arg_index + 1] = arg_type_sig.parameters.values()

    expanded_func = _compile_function(
        f'{func.__name__}_expanded_by_{arg_name}',
        func_sig.replace(parameters=new_params),
        dedent(f'''
            {arg_name} = {arg_type.__name__}{_get_signature_invocation_string(arg_type_sig)}
            return func{_get_signature_invocation_string(func_sig)}
        '''),
        {arg_type.__name__: arg_type, 'func': func, 'NOTHING': attr.NOTHING}
    )
    expanded_func.__doc__ = func.__doc__
    return expanded_func


def expand(arg_name):

    def wrapper(func):
        func_sig = _get_signature(func)
        expanded_func = expand_func_by_argument(func, arg_name)

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            try:
                bound = func_sig.bind(*args, **kwargs)
                return func(*bound.args, **bound.kwargs)
            except TypeError:
                return expanded_func(*args, **kwargs)

        wrapped._func = func
        wrapped._expanded_func = expanded_func
        wrapped._func_sig = func_sig
        wrapped._expanded_func_sig = _get_signature(expanded_func)
        wrapped._expanded_by = arg_name
        return wrapped

    return wrapper


class ExpandParametersMetaclass(BaseTolokaObjectMetaclass):

    def __new__(mcs, name, bases, namespace, **kwargs):
        if 'Parameters' in namespace:
            namespace.setdefault('__annotations__', {})['parameters'] = namespace['Parameters']
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        cls.__init__ = expand('parameters')(cls.__init__)

        return cls


class BaseParameters(BaseTolokaObject, metaclass=ExpandParametersMetaclass):
    class Parameters(BaseTolokaObject):
        pass
