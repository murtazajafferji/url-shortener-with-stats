import pytest
from src.random_id import generate_auth_token
from datetime import datetime, timezone

@pytest.fixture
def stats_path():
    return "/{}/stats"

@pytest.fixture
def redirect_path():
    return "/{}"

def test_stats_url_does_not_exist(client, stats_path, create_url):
    url_id, auth_token = create_url
    response = client.get(stats_path.format("non_existent"), headers={'Authorization': auth_token})
    assert response.status_code == 404


def test_stats_invalid_auth_token(client, stats_path, create_url):
    url_id, auth_token = create_url
    invalid_auth_token = 'invalid_auth_token'
    response = client.get(stats_path.format(url_id), headers={'Authorization': invalid_auth_token})
    assert response.status_code == 403


def test_stats_no_auth_token(client, stats_path, create_url):
    url_id, auth_token = create_url
    response = client.get(stats_path.format(url_id))
    assert response.status_code == 403


def test_stats_visit(client, stats_path, redirect_path, create_url):
    url_id, auth_token = create_url
    response = client.get(stats_path.format(url_id))

    client.get(redirect_path.format(url_id))
    client.get(redirect_path.format(url_id))
    response = client.get(stats_path.format(url_id), headers={'Authorization': auth_token})
    print(response.data)
    visits = next(iter(response.json.values()))

    assert visits == 2
    assert response.status_code == 200


def test_stats_url_id_expired(client, data_store, stats_path, create_url):
    url_id, auth_token = create_url
    data_store.set_expiration(url_id, datetime.now(timezone.utc))
    response = client.get(stats_path.format(url_id), headers={'Authorization': auth_token})

    assert response.status_code == 410


@pytest.fixture
def create_url(data_store):
    url_id = "hrms3zw"
    redirect_url = "http://www.example.com"
    auth_token = generate_auth_token()
    data_store.create_url(url_id, redirect_url, auth_token)

    yield url_id, auth_token

    data_store.delete_url(url_id)
