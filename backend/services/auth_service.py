from datetime import datetime, timezone, timedelta
import jwt
from django.conf import settings


def create_access_token(user_dict):
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user_dict['id'],
        'email': user_dict['email'],
        'role': user_dict['role'],
        'type': 'access',
        'iat': now,
        'exp': now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')


def create_refresh_token(user_dict):
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user_dict['id'],
        'type': 'refresh',
        'iat': now,
        'exp': now + timedelta(minutes=settings.JWT_REFRESH_TOKEN_LIFETIME),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')


def create_tokens(user_dict):
    return {
        'access_token': create_access_token(user_dict),
        'refresh_token': create_refresh_token(user_dict),
    }


def decode_token(token):
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
