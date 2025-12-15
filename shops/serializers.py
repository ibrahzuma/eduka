from rest_framework import serializers
from .models import Shop, Branch, ShopSettings

class ShopSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSettings
        fields = '__all__'
        read_only_fields = ('shop',)

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ('shop', 'created_at')

class ShopSerializer(serializers.ModelSerializer):
    settings = ShopSettingsSerializer(read_only=True)
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at')

    def create(self, validated_data):
        shop = Shop.objects.create(**validated_data)
        # Create default settings
        ShopSettings.objects.create(shop=shop)
        # Create main branch
        Branch.objects.create(shop=shop, name="Main Branch", is_main=True)
        return shop
