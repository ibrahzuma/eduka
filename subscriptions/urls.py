from django.urls import path
from . import views
from .api_views import SubscriptionPlanListView

urlpatterns = [
    path('initiate-payment/', views.InitiatePaymentView.as_view(), name='initiate_payment'),
    path('check-status/<int:payment_id>/', views.CheckPaymentStatusView.as_view(), name='check_payment_status'),
    path('api/status/', views.SubscriptionStatusAPIView.as_view(), name='api_sub_status'),
    path('api/plans/', SubscriptionPlanListView.as_view(), name='api_sub_plans'),
]
