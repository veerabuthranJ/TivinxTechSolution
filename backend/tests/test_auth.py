import pytest


class TestRegistration:
    def test_register_success(self, api_client):
        response = api_client.post('/api/auth/register/', {
            'full_name': 'Test NewUser',
            'email': 'newuser@test.com',
            'password': 'StrongPass1!',
            'confirm_password': 'StrongPass1!',
        }, format='json')
        assert response.status_code == 201
        assert response.data['user']['status'] == 'PENDING'
        assert response.data['user']['role'] == 'USER'

    def test_register_duplicate_email(self, api_client, create_user):
        create_user(email='dup@test.com')
        response = api_client.post('/api/auth/register/', {
            'full_name': 'Test Dup',
            'email': 'dup@test.com',
            'password': 'StrongPass1!',
            'confirm_password': 'StrongPass1!',
        }, format='json')
        assert response.status_code == 409

    def test_register_missing_fields(self, api_client):
        response = api_client.post('/api/auth/register/', {}, format='json')
        assert response.status_code == 400
        assert 'errors' in response.data

    def test_register_password_mismatch(self, api_client):
        response = api_client.post('/api/auth/register/', {
            'full_name': 'Test Mismatch',
            'email': 'mismatch@test.com',
            'password': 'StrongPass1!',
            'confirm_password': 'DifferentPass!',
        }, format='json')
        assert response.status_code == 400
        assert 'confirm_password' in response.data['errors']


class TestLogin:
    def test_login_approved_user(self, api_client, create_user):
        create_user(email='approved@test.com', status='APPROVED')
        response = api_client.post('/api/auth/login/', {
            'email': 'approved@test.com',
            'password': 'TestPass123!',
        }, format='json')
        assert response.status_code == 200
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data
        assert response.data['user']['status'] == 'APPROVED'

    def test_login_pending_user(self, api_client, create_user):
        create_user(email='pending@test.com', status='PENDING')
        response = api_client.post('/api/auth/login/', {
            'email': 'pending@test.com',
            'password': 'TestPass123!',
        }, format='json')
        assert response.status_code == 403
        assert 'awaiting' in response.data['error'].lower()

    def test_login_rejected_user(self, api_client, create_user):
        create_user(email='rejected@test.com', status='REJECTED')
        response = api_client.post('/api/auth/login/', {
            'email': 'rejected@test.com',
            'password': 'TestPass123!',
        }, format='json')
        assert response.status_code == 403
        assert 'not been approved' in response.data['error'].lower()

    def test_login_wrong_password(self, api_client, create_user):
        create_user(email='wrongpw@test.com')
        response = api_client.post('/api/auth/login/', {
            'email': 'wrongpw@test.com',
            'password': 'WrongPassword!',
        }, format='json')
        assert response.status_code == 401

    def test_login_nonexistent_user(self, api_client):
        response = api_client.post('/api/auth/login/', {
            'email': 'nobody@test.com',
            'password': 'SomePass123!',
        }, format='json')
        assert response.status_code == 401


class TestMe:
    def test_get_me_authenticated(self, api_client, user_headers):
        response = api_client.get('/api/auth/me/', **user_headers)
        assert response.status_code == 200
        assert 'user' in response.data

    def test_get_me_unauthenticated(self, api_client):
        response = api_client.get('/api/auth/me/')
        assert response.status_code == 401


class TestChangePassword:
    def test_change_password(self, api_client, create_user):
        create_user(email='changepw@test.com', password='OldPass123!')
        login_resp = api_client.post('/api/auth/login/', {
            'email': 'changepw@test.com',
            'password': 'OldPass123!',
        }, format='json')
        token = login_resp.data['access_token']
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        response = api_client.post('/api/auth/change-password/', {
            'current_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'confirm_password': 'NewPass456!',
        }, format='json', **headers)
        assert response.status_code == 200

        # Verify new password works
        login_resp2 = api_client.post('/api/auth/login/', {
            'email': 'changepw@test.com',
            'password': 'NewPass456!',
        }, format='json')
        assert login_resp2.status_code == 200
