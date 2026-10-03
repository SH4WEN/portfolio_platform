from django.urls import path
from apps.portfolios import views

app_name = 'portfolios'

urlpatterns = [
    # Public portfolio route
    path('p/<slug:slug>/', views.public_portfolio_view, name='public_portfolio'),
    
    # Dashboard item management
    path('dashboard/projects/create/', views.project_create_view, name='project_create'),
    path('dashboard/projects/<int:pk>/edit/', views.project_edit_view, name='project_edit'),
    path('dashboard/projects/<int:pk>/delete/', views.project_delete_view, name='project_delete'),
    
    path('dashboard/skills/create/', views.skill_create_view, name='skill_create'),
    path('dashboard/skills/<int:pk>/edit/', views.skill_edit_view, name='skill_edit'),
    path('dashboard/skills/<int:pk>/delete/', views.skill_delete_view, name='skill_delete'),
    
    path('dashboard/experiences/create/', views.experience_create_view, name='experience_create'),
    path('dashboard/experiences/<int:pk>/edit/', views.experience_edit_view, name='experience_edit'),
    path('dashboard/experiences/<int:pk>/delete/', views.experience_delete_view, name='experience_delete'),
    
    path('dashboard/education/create/', views.education_create_view, name='education_create'),
    path('dashboard/education/<int:pk>/edit/', views.education_edit_view, name='education_edit'),
    path('dashboard/education/<int:pk>/delete/', views.education_delete_view, name='education_delete'),
]
