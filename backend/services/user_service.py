import math
from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from database.connection import get_collection


def serialize_user(user_doc):
    if user_doc is None:
        return None
    user = dict(user_doc)
    user['id'] = str(user.pop('_id'))
    user.pop('password_hash', None)
    for field in ('created_at', 'updated_at', 'approved_at', 'rejected_at', 'disabled_at'):
        if field in user and isinstance(user[field], datetime):
            user[field] = user[field].isoformat()
    return user


def create_user(full_name, email, password_hash, role='USER', status='PENDING'):
    collection = get_collection('users')
    now = datetime.now(timezone.utc)
    user_doc = {
        'full_name': full_name,
        'email': email,
        'password_hash': password_hash,
        'role': role,
        'status': status,
        'created_at': now,
        'updated_at': now,
    }
    result = collection.insert_one(user_doc)
    user_doc['_id'] = result.inserted_id
    return serialize_user(user_doc)


def get_user_by_email(email):
    collection = get_collection('users')
    user_doc = collection.find_one({'email': email})
    return serialize_user(user_doc)


def get_user_by_id(user_id_str):
    try:
        oid = ObjectId(user_id_str)
    except (InvalidId, TypeError):
        return None
    collection = get_collection('users')
    user_doc = collection.find_one({'_id': oid})
    return serialize_user(user_doc)


def get_user_raw_by_email(email):
    collection = get_collection('users')
    return collection.find_one({'email': email})


def get_user_raw_by_id(user_id_str):
    try:
        oid = ObjectId(user_id_str)
    except (InvalidId, TypeError):
        return None
    collection = get_collection('users')
    return collection.find_one({'_id': oid})


def update_user(user_id_str, update_data):
    try:
        oid = ObjectId(user_id_str)
    except (InvalidId, TypeError):
        return None
    collection = get_collection('users')
    update_data['updated_at'] = datetime.now(timezone.utc)
    collection.update_one({'_id': oid}, {'$set': update_data})
    return get_user_by_id(user_id_str)


def list_users(status=None, search=None, page=1, page_size=20):
    collection = get_collection('users')
    query = {}
    if status:
        query['status'] = status
    if search:
        query['$or'] = [
            {'full_name': {'$regex': search, '$options': 'i'}},
            {'email': {'$regex': search, '$options': 'i'}},
        ]
    total = collection.count_documents(query)
    pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    cursor = collection.find(query).sort('created_at', -1).skip(skip).limit(page_size)
    results = [serialize_user(doc) for doc in cursor]
    return {
        'results': results,
        'count': total,
        'page': page,
        'pages': pages,
    }


def get_pending_users():
    collection = get_collection('users')
    cursor = collection.find({'status': 'PENDING'}).sort('created_at', -1)
    return [serialize_user(doc) for doc in cursor]


def count_users_by_status():
    collection = get_collection('users')
    pipeline = [
        {'$group': {'_id': '$status', 'count': {'$sum': 1}}}
    ]
    result = list(collection.aggregate(pipeline))
    counts = {item['_id']: item['count'] for item in result}
    total = sum(counts.values())
    return {
        'total': total,
        'APPROVED': counts.get('APPROVED', 0),
        'PENDING': counts.get('PENDING', 0),
        'REJECTED': counts.get('REJECTED', 0),
        'DISABLED': counts.get('DISABLED', 0),
    }
