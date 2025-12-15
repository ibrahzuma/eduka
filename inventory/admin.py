from django.contrib import admin
from .models import Category, Product, Stock

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop')
    list_filter = ('shop',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'product_type', 'selling_price', 'sku')
    list_filter = ('shop', 'product_type')
    search_fields = ('name', 'sku', 'barcode')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'branch', 'quantity')
    list_filter = ('branch__shop', 'branch')
