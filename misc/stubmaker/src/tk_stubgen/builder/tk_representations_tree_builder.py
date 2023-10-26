import inspect
from typing import Any

import attr
from stubmaker.builder.common import BaseDefinition, Node
from stubmaker.builder.representations_tree_builder import RepresentationsTreeBuilder

from .definitions.expanded_function_def import ExpandedFunctionDef


class TolokaKitRepresentationTreeBuilder(RepresentationsTreeBuilder):

    def __init__(self, *args, type_ignored_modules=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_ignored_modules = set() if type_ignored_modules is None else type_ignored_modules

    def get_function_definition(self, node: Node) -> BaseDefinition:
        if node.obj.__dict__.get('_expanded_func_sig'):
            return ExpandedFunctionDef(node, self)
        else:
            return super().get_function_definition(node)

    def get_literal(self, node):
        if inspect.isclass(node.obj) and 'BaseComponentOr' in str(node.obj.__name__) and hasattr(node.obj, 'union_type'):
            return super().get_literal(self.create_node_for_object(node.namespace, None, node.obj.union_type))

        # Since attrs>=22.2.0 NOTHING is enum field instead of a singleton object, but the enum itself (_Nothing) is not
        # accessible correctly due to the attrs stub files. Therefore, stubs for the NOTHING object can not be generated
        # correctly using current fullpath syntax
        if node.obj is attr.NOTHING:
            node.obj = ...

        # stubmaker does not support forward references properly
        if isinstance(node.obj, str) and node.obj == 'typing.ClassVar[Retry]':
            node.obj = Any

        return super().get_literal(node)
