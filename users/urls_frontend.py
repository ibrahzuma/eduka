from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_frontend

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('register/', views_frontend.RegisterView.as_view(), name='register'),
    path('logout/', views_frontend.custom_logout_view, name='logout'),
    path('roles/', views_frontend.RoleListView.as_view(), name='role_list'),
    path('roles/create/', views_frontend.RoleCreateView.as_view(), name='role_create'),
    path('employees/', views_frontend.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views_frontend.EmployeeCreateView.as_view(), name='employee_create'),
    path('profile/', views_frontend.ProfileView.as_view(), name='profile'),
    # ... other API urls ...
]




