from datetime import datetime, timezone
from database.connection import get_collection


def log_action(action, performed_by, target_id=None, target_type=None, details=None):
    collection = get_collection('audit_logs')
    doc = {
        'action': action,
        'performed_by': performed_by,
        'target_id': target_id,
        'target_type': target_type,
        'details': details,
        'created_at': datetime.now(timezone.utc),
    }
    collection.insert_one(doc)


def get_recent_logs(limit=20):
    collection = get_collection('audit_logs')
    cursor = collection.find().sort('created_at', -1).limit(limit)
    logs = []
    for doc in cursor:
        log = dict(doc)
        log['id'] = str(log.pop('_id'))
        if isinstance(log.get('created_at'), datetime):
            log['created_at'] = log['created_at'].isoformat()
        logs.append(log)
    return logs
