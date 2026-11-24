from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from services import category_service, audit_service
from apps.authentication.decorators import admin_required
from database.connection import get_collection


@api_view(['GET'])
def list_categories(request):
    categories = category_service.list_categories()
    return Response({'results': categories, 'count': len(categories)}, status=status.HTTP_200_OK)


@api_view(['POST'])
@admin_required
def admin_create_category(request):
    name = (request.data.get('name') or '').strip()
    description = (request.data.get('description') or '').strip()

    if not name:
        return Response({'error': 'Category name is required.'}, status=status.HTTP_400_BAD_REQUEST)

    existing = category_service.get_category_by_name(name)
    if existing:
        return Response({'error': 'A category with this name already exists.'}, status=status.HTTP_409_CONFLICT)

    category = category_service.create_category(name, description)
    audit_service.log_action('CATEGORY_CREATED', request.user_data['id'], target_id=category['id'], target_type='category', details=name)
    return Response({'message': 'Category created.', 'category': category}, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@admin_required
def admin_category_detail(request, category_id):
    category = category_service.get_category_by_id(category_id)
    if not category:
        return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        content_count = get_collection('content').count_documents({'category_id': category_id})
        if content_count > 0:
            return Response(
                {'error': f'Cannot delete category. {content_count} content items are using it.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        category_service.delete_category(category_id)
        audit_service.log_action('CATEGORY_DELETED', request.user_data['id'], target_id=category_id, target_type='category', details=category['name'])
        return Response({'message': 'Category deleted.'}, status=status.HTTP_200_OK)

    # PUT
    update = {}
    if 'name' in request.data:
        new_name = request.data['name'].strip()
        if not new_name:
            return Response({'error': 'Category name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        existing = category_service.get_category_by_name(new_name)
        if existing and existing['id'] != category_id:
            return Response({'error': 'A category with this name already exists.'}, status=status.HTTP_409_CONFLICT)
        update['name'] = new_name
    if 'description' in request.data:
        update['description'] = request.data['description'].strip()

    updated = category_service.update_category(category_id, update)
    audit_service.log_action('CATEGORY_UPDATED', request.user_data['id'], target_id=category_id, target_type='category')
    return Response({'message': 'Category updated.', 'category': updated}, status=status.HTTP_200_OK)
