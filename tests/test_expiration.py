import pytest
from src.random_id import generate_auth_token
from datetime import datetime, timedelta, timezone

def test_expiration_is_set(data_store, create_url):
    url_id, auth_token = create_url
    expire_time = data_store.get_expiration(url_id)

    expire_time_date = datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S')
    expiration_date_expected = datetime.now(timezone.utc) + timedelta(days=30) # TODO: Load from configuration value

    assert expire_time_date.date() == expiration_date_expected.date()


@pytest.fixture
def create_url(data_store):
    url_id = "hrms3zw"
    redirect_url = "http://www.example.com"
    auth_token = generate_auth_token()
    data_store.create_url(url_id, redirect_url, auth_token)
    yield url_id, auth_token

    data_store.delete_url(url_id)