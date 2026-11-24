import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


def test_health_check(client):
    response = client.get('/api/health/')
    assert response.status_code in [200, 503]
    assert 'status' in response.data
    assert 'database' in response.data
