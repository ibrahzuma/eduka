from django.contrib import admin
from .models import SubscriptionPlan, ShopSubscription, SubscriptionPayment

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_monthly', 'max_shops', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ShopSubscription)
class ShopSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('shop', 'plan', 'status', 'end_date')
    list_filter = ('status', 'plan')
    search_fields = ('shop__name',)

@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'status', 'created_at')
