from django.urls import path
from .views import InitiatePaymentView, CheckPaymentStatusView, SubscriptionStatusAPIView

urlpatterns = [
    path('pay/initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('pay/status/<int:payment_id>/', CheckPaymentStatusView.as_view(), name='check_payment_status'),
    path('status/check/', SubscriptionStatusAPIView.as_view(), name='check_subscription_status'),
]
