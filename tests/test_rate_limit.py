import pytest
from src.random_id import generate_auth_token
from datetime import datetime, timezone

@pytest.fixture
def redirect_path():
    return "/{}"

def test_rate_limit(client, redirect_path):
    for lp in range(100):
        response = client.get(redirect_path.format("non_existent"))
    assert response.status_code == 429
