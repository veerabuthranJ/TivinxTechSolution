from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_published_content, name='list-published-content'),
    path('search/', views.search_content, name='search-content'),
    path('<str:content_id>/', views.get_published_content, name='get-published-content'),
]
