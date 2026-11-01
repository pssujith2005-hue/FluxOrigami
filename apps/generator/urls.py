from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workspace/', views.workspace_view, name='workspace'),
    path('api/library/folder/create/', views.create_folder, name='api_create_folder'),
    # API Endpoints
    path('api/generate/', views.generate_endpoint, name='api_generate'),
    path('api/history/', views.get_history, name='api_history'),
    path('api/library/save/', views.save_component, name='api_save_component'),
    path('api/library/', views.get_library, name='api_get_library'),
]