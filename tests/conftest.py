import pytest

from src.data import SqliteDataStore
from src import init_app


@pytest.fixture
def data_store(app):
    # TODO: Use a separate test data store for testing
    data_store = SqliteDataStore()
    yield data_store
    data_store.clear_data()


@pytest.fixture
def app():
    return init_app()


@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client