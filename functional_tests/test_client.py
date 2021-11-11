def test_token(token):
    assert token


def test_authentification(client):
    assert client.get_requester()
