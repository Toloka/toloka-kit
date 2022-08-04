import httpx


def check_headers(request, expected_headers):
    if isinstance(request, httpx.Request):
        assert set((key.lower(), value.lower()) for key, value in expected_headers.items()) <= request.headers.items()
    else:
        assert expected_headers.items() <= request._request.headers.items()
