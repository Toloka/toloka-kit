__all__ = [
    'TolokaKitMarkdownViewer',
]
from io import StringIO

from stubmaker.viewers.common import add_inherited_singledispatchmethod
from stubmaker.viewers.markdown_viewer import (
    MarkdownViewer,
    parameter_html_description,
    get_examples_from_docstring,
    get_markdown_page,
)
from ..builder.definitions import ExpandedFunctionDef
from stubmaker.builder.definitions import FunctionDef
from stubmaker.viewers.util import replace_representations_in_signature


@add_inherited_singledispatchmethod(method_name='view', implementation_prefix='view_')
class TolokaKitMarkdownViewer(MarkdownViewer):

    def is_markdown_needed_for_function(self, function_def: FunctionDef):
        parent_call_result = super().is_markdown_needed_for_function(function_def)
        return parent_call_result and function_def.name not in ['structure', 'unstructure']

    def get_definition_markdown_signature(self, function_def: FunctionDef):
        if isinstance(function_def, ExpandedFunctionDef):
            return self.get_definition_markdown_signature(function_def.expanded_func)
        return super(TolokaKitMarkdownViewer, self).get_definition_markdown_signature(function_def)

    def view_expanded_function_definition(self, expanded_function_definition: ExpandedFunctionDef):
        sio = StringIO()

        if expanded_function_definition.docstring:
            parsed_expanded_docstring = (
                expanded_function_definition.expanded_by_class_definition.docstring and
                expanded_function_definition.expanded_by_class_definition.docstring.get_parsed()
            )

            parsed_docstring = expanded_function_definition.docstring.get_parsed()
            if parsed_docstring.short_description:
                sio.write(f'{parsed_docstring.short_description}\n\n')
            if parsed_docstring.long_description:
                sio.write(f'\n{parsed_docstring.long_description}\n\n')

            expanded_func_signature = replace_representations_in_signature(
                expanded_function_definition.expanded_func.signature, self)
            func_signature = replace_representations_in_signature(
                expanded_function_definition.signature, self)

            if parsed_docstring.params:
                sio.write('## Parameters Description\n\n')
                sio.write(self._ATTRIBUTES_TABLE)
                for param in parsed_docstring.params:
                    if param.arg_name == expanded_function_definition.obj._expanded_by and parsed_expanded_docstring:
                        for expanded_param in parsed_expanded_docstring.params:
                            annotation = (
                                expanded_func_signature.parameters.get(expanded_param.arg_name) and
                                expanded_func_signature.parameters[expanded_param.arg_name].annotation
                            )
                            str_annotation = self.add_markdown_crosslinks(annotation)

                            sio.write(
                                f'`{expanded_param.arg_name}`|**{str_annotation or "-"}**|{parameter_html_description(expanded_param.description)}\n')
                    else:
                        annotation = func_signature.parameters.get(param.arg_name) and func_signature.parameters[
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
                if func_signature and func_signature.return_annotation:
                    annotation = func_signature.return_annotation
                    sio.write(f'  {self.add_markdown_crosslinks(annotation)}\n')
                else:
                    sio.write(f'  {ret.type_name}\n')

            sio.write(get_examples_from_docstring(parsed_docstring))
        return get_markdown_page(
            expanded_function_definition.name, expanded_function_definition.full_name, sio.getvalue(),
            source_link=self.source_link_finder(
                expanded_function_definition.original_func
            ) if self.source_link_finder else None,
        )
