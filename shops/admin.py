from django.contrib import admin
from .models import Shop, ShopSettings, Branch

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1

class ShopSettingsInline(admin.StackedInline):
    model = ShopSettings
    can_delete = False

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    inlines = [ShopSettingsInline, BranchInline]
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'phone', 'is_main')
    list_filter = ('shop', 'is_main')
