__all__ = [
    'get_markdown_page',
    'parameter_html_description',
    'get_examples_from_docstring',
    'MarkdownViewer',
]
import inspect
import re
import html

from io import StringIO
from doctest import DocTestParser, Example
from itertools import groupby, chain
from typing import Optional, Callable

from stubmaker.viewers.basic_viewer import BasicViewer
from stubmaker.viewers.util import wrap_function_signature, replace_representations_in_signature
from stubmaker.builder.common import BaseRepresentation, BaseDefinition
from stubmaker.builder.definitions import (
    AttributeAnnotationDef,
    AttributeDef,
    DocumentationDef,
    EnumDef,
    FunctionDef,
    ModuleDef,
    BaseClassDef,
)


def get_markdown_page(name, full_name, markdown_view, source_link=None):
    sio = StringIO()
    sio.write(f'# {name}\n')
    sio.write(f'`{full_name}`')
    if source_link:
        sio.write(f' | [Source code]({source_link})')
    sio.write('\n\n')
    sio.write(markdown_view)
    return sio.getvalue()


def parameter_html_description(desc: str) -> str:
    description = html.escape(desc)

    # we need to use <li> tag for list's items instead of *
    description = re.sub(r'(\n|^)\* ', r'</li><li>', description)
    # we shoudn't use \n cause it breaks html
    description = re.sub(r'\n', r' ', description)

    description = f'<p>{description}</p>'
    # TODO: change to *Default value*
    description = re.sub(r'Default value:', r'</p><p>Default value:', description)

    # we need to wrap the list in the <ul></ul> tag
    # here we believe there can be no more than one list in the description
    description = re.sub(r'(<p>.*?)(</li><li>)', r'\g<1><ul><li>', description)
    description = re.sub(r'(<li>.*?)(</p>)', r'\g<1></li></ul></p>', description)

    return description


def get_examples_from_docstring(parsed_docstring):
    sio = StringIO()
    for m in parsed_docstring.meta:
        if m.args[0] == 'examples':
            sio.write('\n**Examples:**\n\n')
            parsed_tokens = filter(None, DocTestParser().parse(m.description))
            for is_example, values in groupby(parsed_tokens, lambda x: isinstance(x, Example)):
                if is_example:
                    sio.write('```python\n')
                    sio.write(''.join(value.source for value in values))
                    sio.write('```\n')
                else:
                    sio.write(''.join(values))

    cur_value = sio.getvalue()
    if cur_value and not cur_value.endswith('\n'):
        sio.write('\n')

    return sio.getvalue()


def is_markdown_needed_for_function(function_def: FunctionDef):
    _BLACKLIST = [
        'structure',
        'unstructure',
        '__init__',
    ]

    return function_def.full_name and not function_def.name.startswith('_') and function_def.name not in _BLACKLIST


class MarkdownViewer(BasicViewer):
    _ATTRIBUTES_TABLE = """| Parameters | Type | Description |
| :----------| :----| :-----------|\n"""

    def __init__(self, source_link_finder: Callable[[BaseDefinition], str] = None):
        self.source_link_finder = source_link_finder

    def add_markdown_crosslinks(self, annotation: Optional[BaseRepresentation]) -> str:
        if not annotation or annotation is inspect.Parameter.empty:
            return ''
        str_annotation = self.view(annotation)
        str_annotation = re.sub(r'[\[\]]', r'\\\g<0>', str_annotation)
        links = {}
        for child in self.traverse(annotation):
            if child.full_name and child.full_name.startswith(child.tree.module_root + '.'):
                links[self.view(child)] = f'[{self.view(child)}]({child.full_name}.md)'
        for key, value in links.items():
            str_annotation = re.sub(r'\b{}\b'.format(key), value, str_annotation)
        return str_annotation

    def get_markdown_files_for_module(self, module_def: ModuleDef):
        used_object_ids = self.get_used_members_ids(module_def)
        for member in self.traverse(module_def):
            if member.id not in used_object_ids:
                continue
            if isinstance(member, (BaseClassDef, EnumDef)) or isinstance(member, FunctionDef) and is_markdown_needed_for_function(member):
                yield member.full_name, self.view(member)

    def iter_over_class_definition(self, class_def: BaseClassDef):
        if class_def.full_name:
            if class_def.docstring:
                yield class_def.docstring

            if class_def.docstring:
                used_param_names = set(param.arg_name for param in class_def.docstring.get_parsed().params)
            else:
                used_param_names = set()

            for member_name, member in chain(class_def.members.items(), class_def.annotations.items()):
                if isinstance(member, (FunctionDef, BaseClassDef, EnumDef)) or member_name in used_param_names:
                    if member_name == '__init__':
                        # __init__ method representations are merged into class markdown representations instead of
                        # being a separate files like other functions
                        yield from self.iter_over(member)
                    yield member

    def iter_over_enum_definition(self, enum_def: EnumDef):
        if enum_def.full_name and not enum_def.full_name.split('.')[-1].startswith('_'):
            yield from enum_def.enum_dict.values()

    def iter_over_function_definition(self, function_def: FunctionDef):
        yield from super().iter_over_function_definition(function_def)

    def view_attribute_annotation_definition(self, attribute_annotation_def: AttributeAnnotationDef):
        return f'{attribute_annotation_def.name}: {self.view(attribute_annotation_def.annotation)}\n'

    def view_attribute_definition(self, attribute_def: AttributeDef):
        return f'{attribute_def.name} = {self.view(attribute_def.value)}\n'

    def view_base_class_definition(self, class_def: BaseClassDef):
        page_sio = StringIO()
        class_doc_sio = StringIO()

        if '__init__' in class_def.members:
            init_member = class_def.members['__init__']
            init_markdown_signature = self.get_definition_markdown_signature(init_member)
            class_doc_sio.write(f'```python\n{class_def.name}{init_markdown_signature}\n```\n\n')

        if class_def.docstring:
            parsed_docstring = class_def.docstring.get_parsed()
            if parsed_docstring.short_description:
                class_doc_sio.write(f'{parsed_docstring.short_description}\n\n')
            if parsed_docstring.long_description:
                class_doc_sio.write(f'\n{parsed_docstring.long_description}\n\n')

            if parsed_docstring.params:
                class_doc_sio.write('## Parameters Description\n\n')
                class_doc_sio.write(self._ATTRIBUTES_TABLE)
                for param in parsed_docstring.params:
                    nested_parameters = param.arg_name.split('.')
                    if len(nested_parameters) > 1:
                        # expanded nested parameter
                        param.args[0] = 'param'
                        param.arg_name = nested_parameters[-1]

                    if param.args[0] == 'attribute':
                        arg_with_annotations = class_def.annotations.get(param.arg_name)
                        str_annotation = ''
                        if arg_with_annotations:
                            annotation = arg_with_annotations.annotation
                            str_annotation = self.add_markdown_crosslinks(annotation)

                        class_doc_sio.write(
                            f'`{param.arg_name}`|**{str_annotation or "-"}**|{parameter_html_description(param.description)}\n')

                    elif param.args[0] == 'param':
                        init_member = class_def.members['__init__']
                        parameter = init_member.get_parameter(param.arg_name)
                        annotation = parameter and parameter.annotation
                        str_annotation = self.add_markdown_crosslinks(annotation)

                        class_doc_sio.write(
                            f'`{param.arg_name}`|**{str_annotation or "-"}**|{parameter_html_description(param.description)}\n')

            class_doc_sio.write(get_examples_from_docstring(parsed_docstring))

        _methods_table = """| Method | Description |
| :------| :-----------|\n"""
        methods_table_sio = StringIO()
        need_table = True
        if class_def.members:
            for rep in sorted(class_def.members.values(), key=lambda x: x.name):
                if isinstance(rep, FunctionDef) and is_markdown_needed_for_function(rep):

                    if need_table:
                        methods_table_sio.write('## Methods Summary\n\n')
                        methods_table_sio.write(_methods_table)
                    need_table = False

                    methods_table_sio.write(f'[{rep.name}]({rep.full_name}.md)| '
                                            f'{rep.docstring and rep.docstring.get_parsed().short_description}\n')

        page_sio.write(
            get_markdown_page(
                class_def.name, class_def.full_name, class_doc_sio.getvalue(),
                source_link=self.source_link_finder(class_def) if self.source_link_finder else None
            )
        )
        page_sio.write(methods_table_sio.getvalue())

        return page_sio.getvalue()

    def view_documentation_definition(self, documentation_def: DocumentationDef):
        return f'"""{inspect.cleandoc(documentation_def.obj).rstrip()}\n"""\n'

    def view_enum_definition(self, enum_def: EnumDef):
        _attributes_table = """| Name | Value | Description |
| :------| :-----------| :----------| \n"""
        sio = StringIO()

        params_description = {}

        if enum_def.docstring:
            parsed_docstring = enum_def.docstring.get_parsed()
            if parsed_docstring.short_description:
                sio.write(f'{parsed_docstring.short_description}\n\n')
            if parsed_docstring.long_description:
                sio.write(f'\n{parsed_docstring.long_description}\n\n')

            if parsed_docstring.params:
                for param in parsed_docstring.params:
                    params_description[param.arg_name] = param.description

        if enum_def.enum_dict:
            sio.write('## Attributes Description\n\n')
            sio.write(_attributes_table)
            for name, literal in enum_def.enum_dict.items():
                description = params_description.get(name, '')
                sio.write(
                    f'`{name}`|{self.view(literal)}|{parameter_html_description(description)}\n')

        return get_markdown_page(
            enum_def.name, enum_def.full_name, sio.getvalue(),
            source_link=self.source_link_finder(enum_def) if self.source_link_finder else None
        )

    def get_definition_markdown_signature(self, function_def: FunctionDef):
        signature = replace_representations_in_signature(function_def.signature, self)
        if not signature.return_annotation or \
                (signature.return_annotation is not inspect.Parameter.empty and not signature.return_annotation.name):
            signature = signature.replace(return_annotation=inspect.Parameter.empty)
        wrapped_signature = wrap_function_signature(signature)
        return wrapped_signature

    def view_function_definition(self, function_def: FunctionDef):
        sio = StringIO()

        sio.write(f'```python\n{function_def.name}{self.get_definition_markdown_signature(function_def)}\n```\n\n')
        signature = replace_representations_in_signature(function_def.signature, self)

        if function_def.docstring:
            parsed_docstring = function_def.docstring.get_parsed()
            if parsed_docstring.short_description:
                sio.write(f'{parsed_docstring.short_description}\n\n')
            if parsed_docstring.long_description:
                sio.write(f'\n{parsed_docstring.long_description}\n\n')

            if parsed_docstring.params:
                sio.write('## Parameters Description\n\n')
                sio.write(self._ATTRIBUTES_TABLE)
                for param in parsed_docstring.params:
                    annotation = function_def.signature.parameters.get(param.arg_name) and signature.parameters[
                        param.arg_name].annotation
                    str_annotation = self.add_markdown_crosslinks(annotation)

                    sio.write(
                        f'`{param.arg_name}`|**{str_annotation or "-"}**|{parameter_html_description(param.description)}\n')

            if parsed_docstring.returns:
                ret = parsed_docstring.returns
                if ret.args[0] == 'returns':
                    sio.write('\n* **Returns:**\n\n')
                elif ret.args[0] == 'yields':
                    sio.write('\n* **Yields:**\n\n')
                sio.write(f'  {ret.description}\n')

                if ret.args[0] == 'returns':
                    sio.write('\n* **Return type:**\n\n')
                elif ret.args[0] == 'yields':
                    sio.write('\n* **Yield type:**\n\n')
                if signature and signature.return_annotation:
                    annotation = signature.return_annotation
                    sio.write(f'  {self.add_markdown_crosslinks(annotation)}\n')
                else:
                    sio.write(f'  {ret.type_name}\n')

            sio.write(get_examples_from_docstring(parsed_docstring))

        return get_markdown_page(
            function_def.name, function_def.full_name, sio.getvalue(),
            source_link=self.source_link_finder(function_def) if self.source_link_finder else None
        )

    def view_module_definition(self, module_def: ModuleDef):
        raise NotImplementedError
