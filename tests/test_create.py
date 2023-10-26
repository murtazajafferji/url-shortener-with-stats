import pytest
from src.random_id import generate_auth_token
from src.validation import validate_url_id
from flask import request
from datetime import datetime, timezone

# TODO: Implement better clean up for test methods. Consider generating unique url_ids per test
@pytest.fixture
def create_path():
    return "/create"


def test_create_no_json_body(client, create_path):
    response = client.post(create_path)
    assert response.status_code == 415


@pytest.mark.parametrize("invalid_inputs", [
    {},
    [],
    ["url"],
    {"invalid": "invalid"},
    {"url": None},
    {"url": 1},
    {"url": "example"},
    {"url": "example."},
    {"url": "example.com"},
    {"url": "https://example"},
    {"url": "https://example.c"},
    {"id": '-', "url": "https://example.com"},
    {"id": '', "url": "https://example.com"},
    {"id": '123456789012345678901', "url": "https://example.com"}
])
def test_create_invalid(client, create_path, invalid_inputs):
    response = client.post(create_path, json=invalid_inputs)
    assert response.status_code == 400, str(invalid_inputs)


def test_create_with_url_id(client, create_path, create_via_post):
    url_id, auth_token, redirect_url, response = create_via_post

    assert response.status_code == 200
    assert response.json["shortUrl"] == f'{get_server_url()}/{url_id}'
    assert response.json["urlId"] == url_id
    assert len(response.json["authToken"]) > 0, "authToken is blank"


def test_create_with_no_url_id(data_store, client, create_path, create_via_post):
    redirect_url = "http://www.example.com"
    response = client.post(create_path, json={"url": redirect_url})
    url_id = response.json["urlId"]

    assert response.status_code == 200
    assert response.json["shortUrl"] == f'{get_server_url()}/{url_id}'
    assert validate_url_id(url_id)
    assert len(response.json["authToken"]) > 0, "authToken is blank"
    data_store.delete_url(url_id)


def test_create_with_duplicate_url_id(data_store, client, create_path):
    url_id = "hrms3zw"
    redirect_url = "http://www.example.com"
    response = client.post(create_path, json={"id": url_id, "url": redirect_url})
    response = client.post(create_path, json={"id": url_id, "url": redirect_url})

    assert response.status_code == 400


def test_create_with_same_redirect_url_different_url_id(data_store, client, create_path):
    url_id_1 = "hrms3zw1"
    url_id_2 = "hrms3zw2"
    redirect_url = "http://www.example.com"
    response_1 = client.post(create_path, json={"id": url_id_1, "url": redirect_url})
    response_2 = client.post(create_path, json={"id": url_id_2, "url": redirect_url})

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    data_store.delete_url(url_id_1)
    data_store.delete_url(url_id_2)


def test_create_url_id_expired(client, data_store, create_path, create_via_post):
    url_id, auth_token, redirect_url, response = create_via_post
    data_store.set_expiration(url_id, datetime.now(timezone.utc))
    response = client.post(create_path, json={"id": url_id, "url": redirect_url})

    assert response.status_code == 200


def test_create(data_store, client, create_path, create_via_post):
    url_id, auth_token, redirect_url, response = create_via_post
    assert response.status_code == 200
    assert response.json["shortUrl"] == f'{get_server_url()}/{url_id}'
    assert response.json["urlId"] == url_id
    assert len(response.json["authToken"]) > 0, "authToken is blank"

def get_server_url():
    server_name = request.environ.get('SERVER_NAME', 'default_server_name')
    server_port = request.environ.get('SERVER_PORT', 'default_server_port')
    url = f"http://{server_name}:{server_port}"
    return url


@pytest.fixture
def create_via_post(data_store, client, create_path):
    url_id = "hrms3zw"
    redirect_url = "http://www.example.com"
    auth_token = generate_auth_token()
    response = client.post(create_path, json={"id": url_id, "url": redirect_url})

    yield url_id, auth_token, redirect_url, response

    data_store.delete_url(url_id)