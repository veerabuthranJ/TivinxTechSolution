from database.connection import get_database


def create_indexes():
    db = get_database()
    db.users.create_index('email', unique=True)
    db.users.create_index('status')
    db.users.create_index('created_at')
    db.content.create_index('category_id')
    db.content.create_index('status')
    db.content.create_index('created_at')
    db.content.create_index([('title', 'text'), ('description', 'text'), ('tags', 'text')])
    db.categories.create_index('name', unique=True)
    db.audit_logs.create_index('created_at')
    db.audit_logs.create_index('action')
