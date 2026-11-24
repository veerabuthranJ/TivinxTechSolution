from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from services import auth_service, user_service


def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        token = auth_header.split(' ', 1)[1]
        payload = auth_service.decode_token(token)
        if not payload or payload.get('type') != 'access':
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user = user_service.get_user_by_id(payload['user_id'])
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
        if user['status'] != 'APPROVED':
            return Response({'error': 'Account not active'}, status=status.HTTP_403_FORBIDDEN)
        request.user_data = user
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        token = auth_header.split(' ', 1)[1]
        payload = auth_service.decode_token(token)
        if not payload or payload.get('type') != 'access':
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        user = user_service.get_user_by_id(payload['user_id'])
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
        if user['status'] != 'APPROVED':
            return Response({'error': 'Account not active'}, status=status.HTTP_403_FORBIDDEN)
        if user['role'] != 'ADMIN':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        request.user_data = user
        return view_func(request, *args, **kwargs)
    return wrapper
