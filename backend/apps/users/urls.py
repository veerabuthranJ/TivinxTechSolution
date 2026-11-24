from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='list-users'),
    path('pending/', views.get_pending_users, name='pending-users'),
    path('<str:user_id>/', views.get_user, name='get-user'),
    path('<str:user_id>/approve/', views.approve_user, name='approve-user'),
    path('<str:user_id>/reject/', views.reject_user, name='reject-user'),
    path('<str:user_id>/disable/', views.disable_user, name='disable-user'),
    path('<str:user_id>/activate/', views.activate_user, name='activate-user'),
]
