from django.urls import path, include
from apps.authentication.views import health_check

urlpatterns = [
    path('api/health/', health_check, name='health-check'),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/admin/users/', include('apps.users.urls')),
    path('api/admin/content/', include('apps.content.urls_admin')),
    path('api/admin/categories/', include('apps.categories.urls_admin')),
    path('api/admin/dashboard/', include('apps.dashboard.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/categories/', include('apps.categories.urls')),
]
