import pytest
from apps.content.utils import extract_video_id, validate_youtube_url


class TestYouTubeUtils:
    def test_standard_url(self):
        assert extract_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ') == 'dQw4w9WgXcQ'

    def test_short_url(self):
        assert extract_video_id('https://youtu.be/dQw4w9WgXcQ') == 'dQw4w9WgXcQ'

    def test_embed_url(self):
        assert extract_video_id('https://www.youtube.com/embed/dQw4w9WgXcQ') == 'dQw4w9WgXcQ'

    def test_shorts_url(self):
        assert extract_video_id('https://www.youtube.com/shorts/dQw4w9WgXcQ') == 'dQw4w9WgXcQ'

    def test_invalid_url(self):
        assert extract_video_id('https://example.com/video') is None

    def test_validate_youtube_url(self):
        assert validate_youtube_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ') is True
        assert validate_youtube_url('https://example.com') is False


class TestContentAPI:
    def test_create_content(self, api_client, admin_headers):
        response = api_client.post('/api/admin/content/', {
            'title': 'Test Video Content',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'A test video',
            'status': 'published',
        }, format='json', **admin_headers)
        assert response.status_code == 201
        assert response.data['content']['youtube_video_id'] == 'dQw4w9WgXcQ'
        assert 'thumbnail_url' in response.data['content']

    def test_list_published_content(self, api_client, admin_headers):
        # Create published content
        api_client.post('/api/admin/content/', {
            'title': 'Test Published',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'status': 'published',
        }, format='json', **admin_headers)
        response = api_client.get('/api/content/')
        assert response.status_code == 200
        assert response.data['count'] >= 1

    def test_unpublished_content_hidden_from_users(self, api_client, admin_headers):
        resp = api_client.post('/api/admin/content/', {
            'title': 'Test Unpublished Hidden',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'status': 'unpublished',
        }, format='json', **admin_headers)
        content_id = resp.data['content']['id']
        # Public endpoint should not return it
        response = api_client.get(f'/api/content/{content_id}/')
        assert response.status_code == 404

    def test_delete_content(self, api_client, admin_headers):
        resp = api_client.post('/api/admin/content/', {
            'title': 'Test To Delete',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        }, format='json', **admin_headers)
        content_id = resp.data['content']['id']
        delete_resp = api_client.delete(f'/api/admin/content/{content_id}/', **admin_headers)
        assert delete_resp.status_code == 200
        # Verify deleted
        get_resp = api_client.get(f'/api/admin/content/{content_id}/', **admin_headers)
        assert get_resp.status_code == 404
