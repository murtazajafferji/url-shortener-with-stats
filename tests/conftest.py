import pytest

from src.data import SqliteDataStore
from src import init_app


@pytest.fixture
def app():
    return init_app()


@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def data_store(app):
    # TODO: Use a separate test data store for testing
    if (SqliteDataStore.instance() is None):
        SqliteDataStore(testing=app.config['TESTING'])
    yield SqliteDataStore.instance()
    SqliteDataStore.instance().clear_data()