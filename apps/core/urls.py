from django.urls import path
from apps.core import views

app_name = 'core'

urlpatterns = [
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),
    path('', views.dashboard_overview, name='dashboard'),
]
