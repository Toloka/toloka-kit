def check_headers(request, expected_headers):
    assert expected_headers.items() <= request._request.headers.items()
