from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'phone', 'loyalty_points', 'debt')
    list_filter = ('shop',)
    search_fields = ('name', 'phone')
