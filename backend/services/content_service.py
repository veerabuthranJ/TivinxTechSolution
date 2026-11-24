import math
from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from database.connection import get_collection


def serialize_content(doc):
    if doc is None:
        return None
    content = dict(doc)
    content['id'] = str(content.pop('_id'))
    for field in ('created_at', 'updated_at'):
        if field in content and isinstance(content[field], datetime):
            content[field] = content[field].isoformat()
    if content.get('category_id'):
        try:
            cat = get_collection('categories').find_one({'_id': ObjectId(content['category_id'])})
            content['category_name'] = cat['name'] if cat else None
        except (InvalidId, TypeError):
            content['category_name'] = None
    else:
        content['category_name'] = None
    return content


def create_content(data_dict):
    collection = get_collection('content')
    now = datetime.now(timezone.utc)
    doc = {
        'title': data_dict['title'],
        'description': data_dict.get('description', ''),
        'youtube_url': data_dict['youtube_url'],
        'youtube_video_id': data_dict['youtube_video_id'],
        'thumbnail_url': data_dict['thumbnail_url'],
        'category_id': data_dict.get('category_id'),
        'tags': data_dict.get('tags', []),
        'status': data_dict.get('status', 'unpublished'),
        'created_by': data_dict.get('created_by'),
        'created_at': now,
        'updated_at': now,
    }
    result = collection.insert_one(doc)
    doc['_id'] = result.inserted_id
    return serialize_content(doc)


def get_content_by_id(content_id_str):
    try:
        oid = ObjectId(content_id_str)
    except (InvalidId, TypeError):
        return None
    collection = get_collection('content')
    doc = collection.find_one({'_id': oid})
    return serialize_content(doc)


def update_content(content_id_str, update_data):
    try:
        oid = ObjectId(content_id_str)
    except (InvalidId, TypeError):
        return None
    collection = get_collection('content')
    update_data['updated_at'] = datetime.now(timezone.utc)
    collection.update_one({'_id': oid}, {'$set': update_data})
    return get_content_by_id(content_id_str)


def delete_content(content_id_str):
    try:
        oid = ObjectId(content_id_str)
    except (InvalidId, TypeError):
        return False
    collection = get_collection('content')
    result = collection.delete_one({'_id': oid})
    return result.deleted_count > 0


def list_content(filters=None, page=1, page_size=20, published_only=False):
    collection = get_collection('content')
    query = {}
    if published_only:
        query['status'] = 'published'
    if filters:
        if filters.get('category_id'):
            query['category_id'] = filters['category_id']
        if filters.get('tags'):
            query['tags'] = {'$in': filters['tags'] if isinstance(filters['tags'], list) else [filters['tags']]}
        if filters.get('status') and not published_only:
            query['status'] = filters['status']
        if filters.get('search'):
            query['$or'] = [
                {'title': {'$regex': filters['search'], '$options': 'i'}},
                {'description': {'$regex': filters['search'], '$options': 'i'}},
            ]
    sort_field = 'created_at'
    sort_dir = -1
    total = collection.count_documents(query)
    pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    cursor = collection.find(query).sort(sort_field, sort_dir).skip(skip).limit(page_size)
    results = [serialize_content(doc) for doc in cursor]
    return {
        'results': results,
        'count': total,
        'page': page,
        'pages': pages,
    }


def search_content(query_text, category_id=None, tags=None, page=1, page_size=20):
    collection = get_collection('content')
    query = {'status': 'published'}
    if query_text:
        query['$text'] = {'$search': query_text}
    if category_id:
        query['category_id'] = category_id
    if tags:
        tag_list = tags if isinstance(tags, list) else [tags]
        query['tags'] = {'$in': tag_list}
    total = collection.count_documents(query)
    pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    cursor = collection.find(query).sort('created_at', -1).skip(skip).limit(page_size)
    results = [serialize_content(doc) for doc in cursor]
    return {
        'results': results,
        'count': total,
        'page': page,
        'pages': pages,
    }


def count_content_by_status():
    collection = get_collection('content')
    pipeline = [
        {'$group': {'_id': '$status', 'count': {'$sum': 1}}}
    ]
    result = list(collection.aggregate(pipeline))
    counts = {item['_id']: item['count'] for item in result}
    total = sum(counts.values())
    return {
        'total': total,
        'published': counts.get('published', 0),
        'unpublished': counts.get('unpublished', 0),
    }
