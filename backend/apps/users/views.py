from datetime import datetime, timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from services import user_service, audit_service
from apps.authentication.decorators import admin_required


@api_view(['GET'])
@admin_required
def list_users(request):
    user_status = request.query_params.get('status')
    search = request.query_params.get('search')
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    result = user_service.list_users(status=user_status, search=search, page=page, page_size=page_size)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@admin_required
def get_pending_users(request):
    users = user_service.get_pending_users()
    return Response({'results': users, 'count': len(users)}, status=status.HTTP_200_OK)


@api_view(['GET'])
@admin_required
def get_user(request, user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'user': user}, status=status.HTTP_200_OK)


@api_view(['POST'])
@admin_required
def approve_user(request, user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    if user['status'] not in ('PENDING', 'REJECTED'):
        return Response({'error': f"Cannot approve a user with status {user['status']}."}, status=status.HTTP_400_BAD_REQUEST)

    updated = user_service.update_user(user_id, {
        'status': 'APPROVED',
        'approved_at': datetime.now(timezone.utc),
        'approved_by': request.user_data['id'],
    })
    audit_service.log_action('USER_APPROVED', request.user_data['id'], target_id=user_id, target_type='user')
    return Response({'message': 'User approved successfully.', 'user': updated}, status=status.HTTP_200_OK)


@api_view(['POST'])
@admin_required
def reject_user(request, user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    if user['status'] != 'PENDING':
        return Response({'error': f"Cannot reject a user with status {user['status']}."}, status=status.HTTP_400_BAD_REQUEST)

    reason = request.data.get('reason', '')
    updated = user_service.update_user(user_id, {
        'status': 'REJECTED',
        'rejected_at': datetime.now(timezone.utc),
        'rejected_by': request.user_data['id'],
        'rejection_reason': reason,
    })
    audit_service.log_action('USER_REJECTED', request.user_data['id'], target_id=user_id, target_type='user', details=reason)
    return Response({'message': 'User rejected.', 'user': updated}, status=status.HTTP_200_OK)


@api_view(['POST'])
@admin_required
def disable_user(request, user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    if user['status'] != 'APPROVED':
        return Response({'error': f"Cannot disable a user with status {user['status']}."}, status=status.HTTP_400_BAD_REQUEST)
    if user['role'] == 'ADMIN' and user['id'] == request.user_data['id']:
        return Response({'error': 'Cannot disable your own admin account.'}, status=status.HTTP_400_BAD_REQUEST)

    updated = user_service.update_user(user_id, {
        'status': 'DISABLED',
        'disabled_at': datetime.now(timezone.utc),
    })
    audit_service.log_action('USER_DISABLED', request.user_data['id'], target_id=user_id, target_type='user')
    return Response({'message': 'User disabled.', 'user': updated}, status=status.HTTP_200_OK)


@api_view(['POST'])
@admin_required
def activate_user(request, user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    if user['status'] not in ('DISABLED', 'REJECTED'):
        return Response({'error': f"Cannot activate a user with status {user['status']}."}, status=status.HTTP_400_BAD_REQUEST)

    updated = user_service.update_user(user_id, {
        'status': 'APPROVED',
        'approved_at': datetime.now(timezone.utc),
        'approved_by': request.user_data['id'],
    })
    audit_service.log_action('USER_ACTIVATED', request.user_data['id'], target_id=user_id, target_type='user')
    return Response({'message': 'User activated.', 'user': updated}, status=status.HTTP_200_OK)
