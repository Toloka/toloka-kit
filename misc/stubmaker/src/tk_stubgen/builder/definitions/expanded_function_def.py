import inspect
from typing import overload

from stubmaker.builder.definitions import FunctionDef, ClassDef
from stubmaker.builder.common import Node, BaseRepresentationsTreeBuilder
from stubmaker.builder.literals import ReferenceLiteral


class ExpandedFunctionDef(FunctionDef):
    def __init__(self, node: Node, tree: BaseRepresentationsTreeBuilder):
        super().__init__(node, tree)
        self.type_literal = ReferenceLiteral(tree.create_node_for_object(self.namespace, None, overload), self.tree)
        node.obj._expanded_func.__globals__.update(node.obj._func.__globals__)
        self.original_func = FunctionDef(tree.create_node_for_object(node.namespace, node.name, node.obj._func), tree)
        self.expanded_func = FunctionDef(
            tree.create_node_for_object(node.namespace, node.name, node.obj._expanded_func), tree
        )
        expanded_obj = self.get_expanded_obj()
        self.expanded_by_class_definition = ClassDef(tree.create_node_for_object('', '', expanded_obj), tree)

    def get_expanded_obj(self):
        expanded_obj = self.signature.parameters[self.obj._expanded_by].annotation.obj
        if str(expanded_obj).startswith('typing.Optional') or str(expanded_obj).startswith('typing.Union'):
            return expanded_obj.__args__[0] or expanded_obj.__args__[1]
        return expanded_obj

    def get_parameter(self, arg_name: str) -> inspect.Parameter:
        return self.original_func.get_parameter(arg_name) or self.expanded_func.get_parameter(arg_name)

    @property
    def expand_is_redundant(self):
        """Checks if expand has no effect.

        Expand is considered redundant if expanded object has no parameters and it is optional in original method
        signature. In this case expanded version will never be called.

        Example:
            >>> class Parameters:
            >>>     pass
            >>> @expand
            >>> def func(parameters: Parameters = None):
            >>>     ...
            func will be expanded to:
            >>> def func()
            but original signature is broader.
        """
        if len(self.original_func.signature.parameters) <= len(self.expanded_func.signature.parameters):
            return False

        expanded_parameter = self.original_func.signature.parameters[self.obj._expanded_by]
        return expanded_parameter.default is not inspect.Parameter.empty
