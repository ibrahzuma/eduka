from django.urls import path
from .views_frontend import (
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductImportView, ProductTemplateDownloadView, 
    PurchaseCreateView, PurchaseListView, PurchaseRecentView,
    CategoryListView, ServiceListView, ServiceCreateView,
    CategoryListView, ServiceListView, ServiceCreateView,
    StockListView, StockManagementView, StockTransferView, InventoryHealthView,
    InventoryAgingView, ABCAnalysisView, ProfitabilityReportView,
    export_stock_excel, export_stock_pdf, export_stock_csv,
    BarcodePrintView
)

urlpatterns = [
    # Products
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/import/', ProductImportView.as_view(), name='product_import'),
    path('products/import/template/', ProductTemplateDownloadView.as_view(), name='product_import_template'),
    path('products/barcode/', BarcodePrintView.as_view(), name='barcode_print'),
    path('products/<int:pk>/barcode/', BarcodePrintView.as_view(), name='product_barcode_print'),
    
    # Purchase
    path('purchase/create/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/list/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase/recent/', PurchaseRecentView.as_view(), name='purchase_recent'),

    path('categories/', CategoryListView.as_view(), name='category_list'),

    # Services
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),

    # Inventory
    # Inventory
    path('stock/', StockListView.as_view(), name='stock_list'),
    path('stock/export/excel/', export_stock_excel, name='stock_export_excel'),
    path('stock/export/csv/', export_stock_csv, name='stock_export_csv'),
    path('stock/export/pdf/', export_stock_pdf, name='stock_export_pdf'),
    path('stock/management/', StockManagementView.as_view(), name='stock_management'),
    path('stock/transfer/', StockTransferView.as_view(), name='stock_transfer'),
    path('health/', InventoryHealthView.as_view(), name='inventory_health'),
    path('aging/', InventoryAgingView.as_view(), name='inventory_aging'),
    path('abc/', ABCAnalysisView.as_view(), name='abc_analysis'),
    path('profitability/', ProfitabilityReportView.as_view(), name='profitability_report'),
]
