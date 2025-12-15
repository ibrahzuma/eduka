from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseItem

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'phone')
    list_filter = ('shop',)

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseItemInline]
    list_display = ('id', 'shop', 'branch', 'supplier', 'status', 'total_cost')
    list_filter = ('shop', 'branch', 'status')
