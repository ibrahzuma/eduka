from django.urls import path
from .views_frontend import (
    PurchaseCreateView, PurchaseListView, PurchaseRecentView,
    SupplierListView, SupplierCreateView, SupplierDetailView, SupplierUpdateView
)

urlpatterns = [
    path('create/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('list/', PurchaseListView.as_view(), name='purchase_list'),
    path('recent/', PurchaseRecentView.as_view(), name='purchase_recent'),
    
    # Supplier URLs
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', SupplierUpdateView.as_view(), name='supplier_update'),
]
