import pytest
from src.random_id import generate_auth_token
from datetime import datetime, timezone

@pytest.fixture
def delete_path():
    return "/{}"

def test_delete_url_does_not_exist(client, delete_path, create_url):
    url_id, auth_token = create_url
    response = client.delete(delete_path.format("non_existent"), headers={'Authorization': auth_token})
    assert response.status_code == 404


def test_delete_invalid_auth_token(client, delete_path, create_url):
    url_id, auth_token = create_url
    invalid_auth_token = 'vOgp8IeXQOWOy5NS'
    response = client.delete(delete_path.format(url_id), url_id, headers={'Authorization': invalid_auth_token})
    assert response.status_code == 403

def test_delete_no_auth_token(client, delete_path, create_url):
    url_id, auth_token = create_url
    response = client.delete(delete_path.format(url_id), url_id)
    assert response.status_code == 403


def test_delete_url_id_expired(client, delete_path, create_url, data_store):
    url_id, auth_token = create_url
    data_store.set_expiration(url_id, datetime.now(timezone.utc))
    response = client.delete(delete_path.format(url_id), headers={'Authorization': auth_token})

    assert response.status_code == 410


def test_delete(client, delete_path, create_url):
    url_id, auth_token = create_url
    response = client.delete(delete_path.format(url_id), headers={'Authorization': auth_token})
    print(response.data)
    assert response.status_code == 204


@pytest.fixture
def create_url(data_store):
    url_id = "hrms3zw"
    redirect_url = "http://www.example.com"
    auth_token = generate_auth_token()
    data_store.create_url(url_id, redirect_url, auth_token)
    yield url_id, auth_token

    data_store.delete_url(url_id)



