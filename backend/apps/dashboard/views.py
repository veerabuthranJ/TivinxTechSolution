from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from services import user_service, content_service, category_service, audit_service
from apps.authentication.decorators import admin_required
from database.connection import get_collection


@api_view(['GET'])
@admin_required
def get_stats(request):
    user_counts = user_service.count_users_by_status()
    content_counts = content_service.count_content_by_status()
    total_categories = category_service.count_categories()
    recent_logs = audit_service.get_recent_logs(limit=10)

    users_col = get_collection('users')
    recent_users_cursor = users_col.find().sort('created_at', -1).limit(5)
    recent_users = [user_service.serialize_user(doc) for doc in recent_users_cursor]

    content_col = get_collection('content')
    recent_content_cursor = content_col.find().sort('created_at', -1).limit(5)
    recent_content = [content_service.serialize_content(doc) for doc in recent_content_cursor]

    return Response({
        'users': user_counts,
        'content': content_counts,
        'total_categories': total_categories,
        'recent_users': recent_users,
        'recent_content': recent_content,
        'recent_activity': recent_logs,
    }, status=status.HTTP_200_OK)
