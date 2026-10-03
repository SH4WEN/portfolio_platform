from django.urls import path
from apps.clients import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list_view, name='client_list'),
    path('create/', views.client_create_view, name='client_create'),
    path('<int:pk>/', views.client_detail_view, name='client_detail'),
    path('<int:pk>/edit/', views.client_edit_view, name='client_edit'),
    path('<int:pk>/delete/', views.client_delete_view, name='client_delete'),
    path('<int:pk>/toggle-publish/', views.client_toggle_publish_view, name='client_toggle_publish'),
]
