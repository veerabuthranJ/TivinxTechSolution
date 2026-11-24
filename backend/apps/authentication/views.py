import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from database.connection import get_database
from services import user_service, auth_service, audit_service
from apps.authentication.decorators import jwt_required


@api_view(['GET'])
def health_check(request):
    try:
        db = get_database()
        db.command('ping')
        return Response({
            'status': 'healthy',
            'database': 'connected'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def register(request):
    data = request.data
    errors = {}

    full_name = (data.get('full_name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    confirm_password = data.get('confirm_password') or ''

    if not full_name:
        errors['full_name'] = 'Full name is required.'
    if not email:
        errors['email'] = 'Email is required.'
    elif not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        errors['email'] = 'Enter a valid email address.'
    if not password:
        errors['password'] = 'Password is required.'
    elif len(password) < 8:
        errors['password'] = 'Password must be at least 8 characters.'
    if password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'

    if errors:
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    existing = user_service.get_user_by_email(email)
    if existing:
        return Response(
            {'errors': {'email': 'An account with this email already exists.'}},
            status=status.HTTP_409_CONFLICT,
        )

    password_hash = make_password(password)
    user = user_service.create_user(
        full_name=full_name,
        email=email,
        password_hash=password_hash,
    )
    audit_service.log_action('USER_REGISTERED', user['id'], target_id=user['id'], target_type='user')

    return Response({
        'message': 'Your registration has been submitted. Please wait for administrator approval.',
        'user': user,
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    email = (request.data.get('email') or '').strip().lower()
    password = request.data.get('password') or ''

    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    raw_user = user_service.get_user_raw_by_email(email)
    if not raw_user:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, raw_user['password_hash']):
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    user_status = raw_user.get('status')

    if user_status == 'PENDING':
        return Response(
            {'error': 'Your account is awaiting administrator approval.'},
            status=status.HTTP_403_FORBIDDEN,
        )
    if user_status == 'REJECTED':
        return Response(
            {'error': 'Your registration has not been approved. Please contact the administrator.'},
            status=status.HTTP_403_FORBIDDEN,
        )
    if user_status == 'DISABLED':
        return Response(
            {'error': 'Your account has been disabled. Please contact the administrator.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    user = user_service.serialize_user(raw_user)
    tokens = auth_service.create_tokens(user)

    return Response({
        'access_token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        'user': user,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@jwt_required
def logout(request):
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def refresh_token(request):
    token = request.data.get('refresh_token') or ''
    if not token:
        return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    payload = auth_service.decode_token(token)
    if not payload or payload.get('type') != 'refresh':
        return Response({'error': 'Invalid or expired refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)

    user = user_service.get_user_by_id(payload['user_id'])
    if not user or user['status'] != 'APPROVED':
        return Response({'error': 'Account not active.'}, status=status.HTTP_403_FORBIDDEN)

    new_access = auth_service.create_access_token(user)
    return Response({'access_token': new_access}, status=status.HTTP_200_OK)


@api_view(['GET'])
@jwt_required
def get_me(request):
    return Response({'user': request.user_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@jwt_required
def change_password(request):
    current_password = request.data.get('current_password') or ''
    new_password = request.data.get('new_password') or ''
    confirm_password = request.data.get('confirm_password') or ''

    if not current_password or not new_password or not confirm_password:
        return Response({'error': 'All password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 8:
        return Response({'error': 'New password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    raw_user = user_service.get_user_raw_by_id(request.user_data['id'])
    if not check_password(current_password, raw_user['password_hash']):
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    new_hash = make_password(new_password)
    user_service.update_user(request.user_data['id'], {'password_hash': new_hash})
    audit_service.log_action('PASSWORD_CHANGED', request.user_data['id'], target_type='user')

    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
