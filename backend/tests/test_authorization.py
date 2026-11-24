import pytest


class TestUserCannotAccessAdmin:
    def test_user_cannot_access_admin_users(self, api_client, user_headers):
        response = api_client.get('/api/admin/users/', **user_headers)
        assert response.status_code == 403

    def test_user_cannot_create_content(self, api_client, user_headers):
        response = api_client.post('/api/admin/content/', {
            'title': 'Test Hacked',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        }, format='json', **user_headers)
        assert response.status_code == 403

    def test_user_cannot_approve_users(self, api_client, user_headers, create_user):
        pending = create_user(email='pendingapproval@test.com', status='PENDING')
        user_id = str(pending['_id'])
        response = api_client.post(f'/api/admin/users/{user_id}/approve/', **user_headers)
        assert response.status_code == 403


class TestAdminAccess:
    def test_admin_can_list_users(self, api_client, admin_headers):
        response = api_client.get('/api/admin/users/', **admin_headers)
        assert response.status_code == 200
        assert 'results' in response.data

    def test_admin_can_approve_user(self, api_client, admin_headers, create_user):
        pending = create_user(email='toapprove@test.com', status='PENDING')
        user_id = str(pending['_id'])
        response = api_client.post(f'/api/admin/users/{user_id}/approve/', **admin_headers)
        assert response.status_code == 200
        assert response.data['user']['status'] == 'APPROVED'

    def test_admin_can_create_content(self, api_client, admin_headers):
        response = api_client.post('/api/admin/content/', {
            'title': 'Test Admin Content',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'Test description',
        }, format='json', **admin_headers)
        assert response.status_code == 201
        assert response.data['content']['title'] == 'Test Admin Content'
