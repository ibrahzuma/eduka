from django.urls import path
from .views_frontend import (
    SaleCreateView, SaleListView, SaleCreditView, SaleRecentView,
    ReturnInwardsView, ReturnOutwardsView, SaleDetailView, SaleDeleteView
)

urlpatterns = [
    # Sales
    path('', SaleListView.as_view(), name='sales_index'), # Added default route
    path('pos/', SaleCreateView.as_view(), name='sale_pos'),
    path('list/', SaleListView.as_view(), name='sale_list'),
    path('credit/', SaleCreditView.as_view(), name='sale_credit'),
    path('recent/', SaleRecentView.as_view(), name='sale_recent'),
    path('invoice/<int:pk>/', SaleDetailView.as_view(), name='sale_invoice'),
    path('delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    
    # Returns (Assuming handled in Sales for now)
    path('returns/inwards/', ReturnInwardsView.as_view(), name='return_inwards'),
    path('returns/outwards/', ReturnOutwardsView.as_view(), name='return_outwards'),
]
