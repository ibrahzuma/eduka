from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_frontend

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('register/', views_frontend.RegisterView.as_view(), name='register'),
    path('logout/', views_frontend.custom_logout_view, name='logout'),
    path('roles/', views_frontend.RoleListView.as_view(), name='role_list'),
    path('roles/create/', views_frontend.RoleCreateView.as_view(), name='role_create'),
    path('roles/<int:pk>/edit/', views_frontend.RoleUpdateView.as_view(), name='role_edit'),
    path('employees/', views_frontend.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views_frontend.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/edit/', views_frontend.EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/suspend/', views_frontend.EmployeeSuspendView.as_view(), name='employee_suspend'),
    path('employees/<int:pk>/delete/', views_frontend.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('profile/', views_frontend.ProfileView.as_view(), name='profile'),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]




