from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from services import content_service, audit_service
from apps.authentication.decorators import admin_required
from apps.content.utils import extract_video_id, get_thumbnail_url, validate_youtube_url


@api_view(['GET'])
def list_published_content(request):
    category = request.query_params.get('category')
    tags = request.query_params.get('tags')
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    filters = {}
    if category:
        filters['category_id'] = category
    if tags:
        filters['tags'] = [t.strip() for t in tags.split(',')]
    result = content_service.list_content(filters=filters, page=page, page_size=page_size, published_only=True)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_published_content(request, content_id):
    content = content_service.get_content_by_id(content_id)
    if not content or content.get('status') != 'published':
        return Response({'error': 'Content not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'content': content}, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_content(request):
    q = request.query_params.get('q', '')
    category = request.query_params.get('category')
    tags = request.query_params.get('tags')
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    tag_list = [t.strip() for t in tags.split(',')] if tags else None
    result = content_service.search_content(q, category_id=category, tags=tag_list, page=page, page_size=page_size)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@admin_required
def admin_list_or_create_content(request):
    if request.method == 'GET':
        search = request.query_params.get('search')
        category = request.query_params.get('category')
        content_status = request.query_params.get('status')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        filters = {}
        if search:
            filters['search'] = search
        if category:
            filters['category_id'] = category
        if content_status:
            filters['status'] = content_status
        result = content_service.list_content(filters=filters, page=page, page_size=page_size)
        return Response(result, status=status.HTTP_200_OK)

    data = request.data
    title = (data.get('title') or '').strip()
    youtube_url = (data.get('youtube_url') or '').strip()

    if not title:
        return Response({'error': 'Title is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not youtube_url:
        return Response({'error': 'YouTube URL is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not validate_youtube_url(youtube_url):
        return Response({'error': 'Invalid YouTube URL.'}, status=status.HTTP_400_BAD_REQUEST)

    video_id = extract_video_id(youtube_url)
    thumbnail_url = get_thumbnail_url(video_id)

    tags = data.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]

    content = content_service.create_content({
        'title': title,
        'description': (data.get('description') or '').strip(),
        'youtube_url': youtube_url,
        'youtube_video_id': video_id,
        'thumbnail_url': thumbnail_url,
        'category_id': data.get('category_id'),
        'tags': tags,
        'status': data.get('status', 'unpublished'),
        'created_by': request.user_data['id'],
    })
    audit_service.log_action('CONTENT_CREATED', request.user_data['id'], target_id=content['id'], target_type='content', details=title)
    return Response({'message': 'Content created.', 'content': content}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@admin_required
def admin_content_detail(request, content_id):
    content = content_service.get_content_by_id(content_id)
    if not content:
        return Response({'error': 'Content not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response({'content': content}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        content_service.delete_content(content_id)
        audit_service.log_action('CONTENT_DELETED', request.user_data['id'], target_id=content_id, target_type='content', details=content['title'])
        return Response({'message': 'Content deleted.'}, status=status.HTTP_200_OK)

    # PUT
    data = request.data
    update = {}
    if 'title' in data:
        update['title'] = data['title'].strip()
    if 'description' in data:
        update['description'] = data['description'].strip()
    if 'youtube_url' in data:
        youtube_url = data['youtube_url'].strip()
        if not validate_youtube_url(youtube_url):
            return Response({'error': 'Invalid YouTube URL.'}, status=status.HTTP_400_BAD_REQUEST)
        video_id = extract_video_id(youtube_url)
        update['youtube_url'] = youtube_url
        update['youtube_video_id'] = video_id
        update['thumbnail_url'] = get_thumbnail_url(video_id)
    if 'category_id' in data:
        update['category_id'] = data['category_id']
    if 'tags' in data:
        tags = data['tags']
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]
        update['tags'] = tags
    if 'status' in data:
        update['status'] = data['status']

    updated = content_service.update_content(content_id, update)
    audit_service.log_action('CONTENT_UPDATED', request.user_data['id'], target_id=content_id, target_type='content')
    return Response({'message': 'Content updated.', 'content': updated}, status=status.HTTP_200_OK)
