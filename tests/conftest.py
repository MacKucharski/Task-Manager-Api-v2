import pytest
from api import api

@pytest.fixture
def client():
    api.testing = True
    with api.test_client() as client:
        yield client