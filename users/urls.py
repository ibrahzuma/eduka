from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, UserManagementAPIView, UserActionAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('manage/', UserManagementAPIView.as_view(), name='api_user_manage'),
    path('action/', UserActionAPIView.as_view(), name='api_user_action'),
]
