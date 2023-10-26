import pytest
from src.random_id import generate_auth_token
from datetime import datetime, timezone

@pytest.fixture
def redirect_path():
    return "/{}"

def test_redirect_url_id_does_not_exist(client, redirect_path):
    response = client.get(redirect_path.format("hrms3zw"))
    assert response.status_code == 404


def test_redirect_url_id_expired(client, data_store, redirect_path, create_url):
    url_id, auth_token = create_url
    data_store.set_expiration(url_id, datetime.now(timezone.utc))
    response = client.get(redirect_path.format(url_id))

    assert response.status_code == 410


# werkzeug.Response does not have a url property. Use location instead
# https://tedboy.github.io/flask/generated/generated/werkzeug.Response.html
def test_redirect_success(client, redirect_path, create_url):
    url_id, redirect_url = create_url
    response = client.get(redirect_path.format(url_id))
    assert response.status_code == 301
    assert response.location == redirect_url


@pytest.fixture
def create_url(data_store):
    url_id = "hrms3zw"
    redirect_url = "http://www.example.com"
    auth_token = generate_auth_token()
    data_store.create_url(url_id, redirect_url, auth_token)

    yield url_id, redirect_url

    data_store.delete_url(url_id)