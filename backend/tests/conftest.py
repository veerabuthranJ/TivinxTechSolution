import pytest
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password
from database.connection import get_database
from datetime import datetime, timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def clean_db():
    yield
    db = get_database()
    db.users.delete_many({'email': {'$regex': r'@test\.com$'}})
    db.content.delete_many({'title': {'$regex': r'^Test '}})
    db.categories.delete_many({'name': {'$regex': r'^Test '}})
    db.audit_logs.delete_many({'performed_by': {'$regex': r'test'}})


@pytest.fixture
def create_user():
    def _create(email='user@test.com', password='TestPass123!', role='USER', status='APPROVED', full_name='Test User'):
        db = get_database()
        user = {
            'full_name': full_name,
            'email': email,
            'password_hash': make_password(password),
            'role': role,
            'status': status,
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc),
        }
        result = db.users.insert_one(user)
        user['_id'] = result.inserted_id
        return user
    return _create


@pytest.fixture
def admin_headers(create_user, api_client):
    create_user(email='admin@test.com', role='ADMIN', status='APPROVED')
    response = api_client.post('/api/auth/login/', {'email': 'admin@test.com', 'password': 'TestPass123!'}, format='json')
    token = response.data['access_token']
    return {'HTTP_AUTHORIZATION': f'Bearer {token}'}


@pytest.fixture
def user_headers(create_user, api_client):
    create_user(email='regularuser@test.com', role='USER', status='APPROVED')
    response = api_client.post('/api/auth/login/', {'email': 'regularuser@test.com', 'password': 'TestPass123!'}, format='json')
    token = response.data['access_token']
    return {'HTTP_AUTHORIZATION': f'Bearer {token}'}
