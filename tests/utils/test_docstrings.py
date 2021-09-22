import pytest
import docstring_parser

from toloka.util._docstrings import inherit_docstrings


@pytest.fixture
def simple_base_class_with_docstring():
    class DummyBase:
        """
        Attributes:
            base_attr: defined in base

        Args:
            base_arg: defined in base

        Examples:
            this is base class example
        """
        class Nested:
            """
            Attributes:
                nested_base_attr: defined in nested dummybase

            Args:
                nested_base_arg: defined in nested dummybase

            Examples:
                this is nested base class example
            """

    def function(self):
        """function

        Returns:
            int: parent return
        """
        return 0

    return DummyBase


@pytest.fixture
def simple_child_class_with_docstring(simple_base_class_with_docstring):
    class Dummy(simple_base_class_with_docstring):
        """short description

        long description

        Attributes:
            base_attr: redefined
            child_attr: ...

        Args:
            base_arg: redefined
            child_arg: ...

        Raises:
            ValueError: child description
            RuntimeError: child description 2

        Examples:
            this is child class example
        """

        class Nested:
            """
            Attributes:
                nested_base_attr: redefined
                nested_child_attr: ...

            Args:
                nested_base_arg: redefined
                nested_child_arg: ...

            Raises:
                ValueError: nested child description
                RuntimeError: nested child description 2

            Examples:
                this is nested child class example
            """

        def function(self):
            """child function

            Returns:
                bool: child return
            """
            return True

    return Dummy


def test_inherit_docstrings_create_correct_docstring(simple_child_class_with_docstring):
    parsed = docstring_parser.google.parse(inherit_docstrings(simple_child_class_with_docstring).__doc__)
    assert len(parsed.params) == 4
    assert parsed.long_description
    assert parsed.short_description
    assert parsed.raises
    assert 'examples' in [meta.args[0] for meta in parsed.meta]


def test_doc_without_description_reconstructed_correctly(simple_base_class_with_docstring):
    assert inherit_docstrings(simple_base_class_with_docstring).__doc__[0] == '\n'


def check_if_meta_is_same(first_meta, second_meta):
    first_meta_dict = {meta.description: meta.__dict__ for meta in first_meta}
    second_meta_dict = {meta.description: meta.__dict__ for meta in second_meta}
    assert first_meta_dict == second_meta_dict


def test_inherit_docstrings_preserves_non_param_child_meta(simple_child_class_with_docstring):
    child_docstring = docstring_parser.google.parse(simple_child_class_with_docstring.__doc__)
    decorated_child_docstring = docstring_parser.google.parse(
        inherit_docstrings(simple_child_class_with_docstring).__doc__
    )

    check_if_meta_is_same(
        [meta for meta in child_docstring.meta if not isinstance(meta, docstring_parser.DocstringParam)],
        [meta for meta in decorated_child_docstring.meta if not isinstance(meta, docstring_parser.DocstringParam)]
    )


def test_inherit_docstrings_preserves_non_param_nested_child_meta(simple_child_class_with_docstring):
    nested_child_docstring = docstring_parser.google.parse(simple_child_class_with_docstring.Nested.__doc__)
    nested_decorated_child_docstring = docstring_parser.google.parse(
        inherit_docstrings(simple_child_class_with_docstring).Nested.__doc__
    )

    check_if_meta_is_same(
        [meta for meta in nested_child_docstring.meta if not isinstance(meta, docstring_parser.DocstringParam)],
        [meta for meta in nested_decorated_child_docstring.meta
            if not isinstance(meta, docstring_parser.DocstringParam)]
    )


def test_inherit_docstrings_preserves_non_param_child_function_meta(simple_child_class_with_docstring):
    child_function_docstring = docstring_parser.google.parse(simple_child_class_with_docstring.function.__doc__)
    decorated_child_function_docstring = docstring_parser.google.parse(
        inherit_docstrings(simple_child_class_with_docstring).function.__doc__
    )

    check_if_meta_is_same(
        [meta for meta in child_function_docstring.meta if not isinstance(meta, docstring_parser.DocstringParam)],
        [meta for meta in decorated_child_function_docstring.meta
            if not isinstance(meta, docstring_parser.DocstringParam)]
    )


def check_if_params_are_joined(joined_params_doc, first_doc, second_doc):
    joined_params = {param.arg_name for param in joined_params_doc.params}
    first_params = {param.arg_name for param in first_doc.params}
    second_params = {param.arg_name for param in second_doc.params}
    assert joined_params == first_params.union(second_params)


def test_inherit_docstrings_joins_params(simple_base_class_with_docstring,
                                         simple_child_class_with_docstring):
    parsed_base_doc = docstring_parser.google.parse(simple_base_class_with_docstring.__doc__)
    parsed_child_doc = docstring_parser.google.parse(simple_child_class_with_docstring.__doc__)
    decorated_parsed_child_doc = docstring_parser.google.parse(
        inherit_docstrings(simple_child_class_with_docstring).__doc__
    )

    check_if_params_are_joined(decorated_parsed_child_doc, parsed_child_doc, parsed_base_doc)


def test_inherit_docstrings_joins_nested_params(simple_base_class_with_docstring,
                                                simple_child_class_with_docstring):
    parsed_base_doc = docstring_parser.google.parse(simple_base_class_with_docstring.Nested.__doc__)
    parsed_child_doc = docstring_parser.google.parse(simple_child_class_with_docstring.Nested.__doc__)
    decorated_parsed_child_doc = docstring_parser.google.parse(
        inherit_docstrings(simple_child_class_with_docstring).Nested.__doc__
    )

    check_if_params_are_joined(decorated_parsed_child_doc, parsed_child_doc, parsed_base_doc)


def check_if_params_overriden(base_params_doc, child_params_doc):
    base_params = {param.arg_name for param in base_params_doc.params}
    for param in child_params_doc.params:
        if param.arg_name in base_params:
            assert param.description == 'redefined'


def test_inherit_docstrings_overrides_params(simple_base_class_with_docstring,
                                             simple_child_class_with_docstring):
    parsed_base_doc = docstring_parser.google.parse(simple_base_class_with_docstring.__doc__)
    parsed_child_doc = docstring_parser.google.parse(inherit_docstrings(simple_child_class_with_docstring).__doc__)

    check_if_params_overriden(parsed_base_doc, parsed_child_doc)


def test_inherit_docstrings_overrides_nested_params(simple_base_class_with_docstring,
                                                    simple_child_class_with_docstring):
    parsed_nested_base_doc = docstring_parser.google.parse(simple_base_class_with_docstring.Nested.__doc__)
    parsed_nested_child_doc = docstring_parser.google.parse(
        inherit_docstrings(simple_child_class_with_docstring).Nested.__doc__)

    check_if_params_overriden(parsed_nested_base_doc, parsed_nested_child_doc)
