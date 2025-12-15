from rest_framework import serializers
from .models import Supplier, PurchaseOrder, PurchaseItem

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ()

class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = PurchaseItem
        fields = '__all__'
        read_only_fields = ('purchase_order',)

class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        # Logic to get shop/branch from user/context
        # Placeholder: assume user is owner or context has branch info
        # This will be handled in ViewSet perform_create
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        for item_data in items_data:
            PurchaseItem.objects.create(purchase_order=purchase_order, **item_data)
        return purchase_order
