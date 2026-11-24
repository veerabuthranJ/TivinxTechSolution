from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_list_or_create_content, name='admin-content-list-create'),
    path('<str:content_id>/', views.admin_content_detail, name='admin-content-detail'),
]
