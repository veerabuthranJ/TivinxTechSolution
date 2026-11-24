import os
from pathlib import Path
from decouple import config as env_config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env_config('DJANGO_SECRET_KEY')

DEBUG = env_config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = env_config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.authentication',
    'apps.users',
    'apps.content',
    'apps.categories',
    'apps.dashboard',
    'apps.audit',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# No Django ORM database — all data in MongoDB via PyMongo
DATABASES = {}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS
FRONTEND_URL = env_config('FRONTEND_URL', default='http://localhost:4200')
CORS_ALLOWED_ORIGINS = [FRONTEND_URL]
CORS_ALLOW_CREDENTIALS = True

# MongoDB
MONGODB_URI = env_config('MONGODB_URI')
MONGODB_DATABASE = env_config('MONGODB_DATABASE', default='content_portal')

# JWT
JWT_SECRET_KEY = env_config('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_LIFETIME = env_config('JWT_ACCESS_TOKEN_LIFETIME', default=30, cast=int)
JWT_REFRESH_TOKEN_LIFETIME = env_config('JWT_REFRESH_TOKEN_LIFETIME', default=1440, cast=int)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True

STATIC_URL = 'static/'
