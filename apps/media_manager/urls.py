from django.urls import path
from apps.media_manager import views

app_name = 'media_manager'

urlpatterns = [
    path('dashboard/files/', views.file_list_view, name='file_list'),
    path('dashboard/files/upload/', views.file_upload_view, name='file_upload'),
    path('dashboard/files/<int:pk>/replace/', views.file_replace_view, name='file_replace'),
    path('dashboard/files/<int:pk>/toggle-visibility/', views.file_toggle_visibility_view, name='file_toggle_visibility'),
    path('dashboard/files/<int:pk>/delete/', views.file_delete_view, name='file_delete'),
    path('dashboard/files/<int:pk>/download/', views.private_file_download_view, name='private_download'),
]
