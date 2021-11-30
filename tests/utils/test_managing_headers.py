from toloka.util._managing_headers import add_headers, caller_context_var, top_level_method_var, low_level_method_var
import contextvars


def test_simple_function():
    @add_headers('TestClient')
    def dummy_func():
        local_ctx = contextvars.copy_context()
        return local_ctx

    ctx = dummy_func()

    assert ctx[caller_context_var] == 'TestClient'
    assert ctx[top_level_method_var] == 'dummy_func'
    assert ctx[low_level_method_var] == 'dummy_func'


def test_complex_function():
    @add_headers('TestClient')
    def dummy_func():
        local_ctx = contextvars.copy_context()
        return local_ctx

    @add_headers('AnotherTestClient')
    def complex_func():
        return dummy_func()

    ctx = complex_func()

    assert ctx[caller_context_var] == 'AnotherTestClient'
    assert ctx[top_level_method_var] == 'complex_func'
    assert ctx[low_level_method_var] == 'dummy_func'
