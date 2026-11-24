from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_create_category, name='admin-create-category'),
    path('<str:category_id>/', views.admin_category_detail, name='admin-category-detail'),
]
