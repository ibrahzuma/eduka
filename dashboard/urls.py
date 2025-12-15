from django.urls import path
from .views import DashboardSummaryView, SuperUserDashboardView

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('superuser/', SuperUserDashboardView.as_view(), name='superuser_dashboard'),
]
