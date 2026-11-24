from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from database.connection import get_collection
from database.indexes import create_indexes
from services import user_service


class Command(BaseCommand):
    help = 'Create the initial admin user and set up database indexes'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, default='admin@company.com')
        parser.add_argument('--password', type=str, default='Admin@123')
        parser.add_argument('--name', type=str, default='System Admin')

    def handle(self, *args, **options):
        create_indexes()
        self.stdout.write('Database indexes created.')

        existing = user_service.get_user_by_email(options['email'])
        if existing:
            self.stdout.write(f"Admin {options['email']} already exists.")
            return

        now = datetime.now(timezone.utc)
        user_doc = {
            'full_name': options['name'],
            'email': options['email'],
            'password_hash': make_password(options['password']),
            'role': 'ADMIN',
            'status': 'APPROVED',
            'created_at': now,
            'updated_at': now,
            'approved_at': now,
            'approved_by': 'system',
        }
        collection = get_collection('users')
        collection.insert_one(user_doc)
        self.stdout.write(self.style.SUCCESS(f"Admin user created: {options['email']}"))
