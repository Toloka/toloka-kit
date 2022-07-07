import inspect

from stubmaker.builder.representations_tree_builder import RepresentationsTreeBuilder
from stubmaker.builder.common import Node, BaseDefinition

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
        return super().get_literal(node)
