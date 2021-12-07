from toloka.client.primitives.retry import PreloadingHTTPAdapter


def test_get_connection_wrapped_once():
    adapter = PreloadingHTTPAdapter()
    adapter.get_connection('fake')
    assert '__wrapped__' not in dir(adapter.get_connection('fake').urlopen.__wrapped__)
