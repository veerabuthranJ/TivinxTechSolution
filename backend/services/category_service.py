from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from database.connection import get_collection


def serialize_category(doc):
    if doc is None:
        return None
    cat = dict(doc)
    cat['id'] = str(cat.pop('_id'))
    for field in ('created_at', 'updated_at'):
        if field in cat and isinstance(cat[field], datetime):
            cat[field] = cat[field].isoformat()
    return cat


def create_category(name, description=''):
    collection = get_collection('categories')
    now = datetime.now(timezone.utc)
    doc = {
        'name': name,
        'description': description,
        'created_at': now,
        'updated_at': now,
    }
    result = collection.insert_one(doc)
    doc['_id'] = result.inserted_id
    return serialize_category(doc)


def get_category_by_id(category_id_str):
    try:
        oid = ObjectId(category_id_str)
    except (InvalidId, TypeError):
        return None
    collection = get_collection('categories')
    doc = collection.find_one({'_id': oid})
    return serialize_category(doc)


def get_category_by_name(name):
    collection = get_collection('categories')
    doc = collection.find_one({'name': name})
    return serialize_category(doc)


def update_category(category_id_str, update_data):
    try:
        oid = ObjectId(category_id_str)
    except (InvalidId, TypeError):
        return None
    collection = get_collection('categories')
    update_data['updated_at'] = datetime.now(timezone.utc)
    collection.update_one({'_id': oid}, {'$set': update_data})
    return get_category_by_id(category_id_str)


def delete_category(category_id_str):
    try:
        oid = ObjectId(category_id_str)
    except (InvalidId, TypeError):
        return False
    collection = get_collection('categories')
    result = collection.delete_one({'_id': oid})
    return result.deleted_count > 0


def list_categories():
    collection = get_collection('categories')
    cursor = collection.find().sort('name', 1)
    return [serialize_category(doc) for doc in cursor]


def count_categories():
    collection = get_collection('categories')
    return collection.count_documents({})
