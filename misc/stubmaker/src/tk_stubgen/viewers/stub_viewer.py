__all__ = [
    'TolokaKitStubViewer',
]

from stubmaker.builder.literals import TypeHintLiteral
from stubmaker.viewers.common import add_inherited_singledispatchmethod
from stubmaker.viewers.stub_viewer import StubViewer
from stubmaker.viewers.util import indent
from ..builder.definitions.expanded_function_def import ExpandedFunctionDef

from io import StringIO
from typing import List, Tuple, Optional


@add_inherited_singledispatchmethod(method_name='iter_over', implementation_prefix='iter_over_')
@add_inherited_singledispatchmethod(method_name='view', implementation_prefix='view_')
class TolokaKitStubViewer(StubViewer):

    def view_expanded_function_definition(self, expanded_function_definition: ExpandedFunctionDef):
        sio = StringIO()
        if expanded_function_definition.expand_is_redundant:
            sio.write(self.view(expanded_function_definition.original_func))
        else:
            sio.write(f'@{self.view(expanded_function_definition.type_literal)}\n')
            sio.write(self.view(expanded_function_definition.original_func))
            sio.write(f'@{self.view(expanded_function_definition.type_literal)}\n')
            sio.write(self.view(expanded_function_definition.expanded_func))
        return sio.getvalue()

    def iter_over_expanded_function_definition(self, expanded_function_definition: ExpandedFunctionDef):
        yield expanded_function_definition.original_func
        yield expanded_function_definition.expanded_func
        yield expanded_function_definition.type_literal

    def _is_module_type_ignored(self, module_name):
        return module_name.split('.')[0] in self.module_context.module_def.tree.type_ignored_modules

    def _write_import(self, module_name: str, sio: StringIO):
        sio.write(f'import {module_name}')
        if self._is_module_type_ignored(module_name):
            sio.write('  # type: ignore')
        sio.write('\n')

    def _write_from_import(self, module_name: str, names: List[Tuple[str, Optional[str]]], sio: StringIO):
        type_ignore_str = '  # type: ignore' if self._is_module_type_ignored(module_name) else ''
        if len(names) > 1:
            names = ',\n'.join(
                f'{name} as {import_as}' if import_as else name for name, import_as in names)
            sio.write(f'from {module_name} import ({type_ignore_str}\n{indent(names)},\n)\n')
        else:
            names = ', '.join(f'{name} as {import_as}' if import_as else name for name, import_as in names)
            sio.write(f'from {module_name} import {names}{type_ignore_str}\n')
