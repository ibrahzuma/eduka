from rest_framework import viewsets, permissions
from .models import Category, Product, Stock
from .serializers import CategorySerializer, ProductSerializer, StockSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return Category.objects.all()
        return Category.objects.filter(shop__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        shop = None
        if getattr(user, 'shop', None):
            shop = user.shop
        elif hasattr(user, 'shops') and user.shops.exists():
            shop = user.shops.first()
        elif hasattr(user, 'employee_profile'):
            shop = user.employee_profile.shop
        
        if shop:
            serializer.save(shop=shop)
        else:
            # Fallback or error if no shop? DRF will error if shop is mandatory and not provided.
            # But normally we expect a shop here.
            pass

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(shop__owner=user)

class StockViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StockSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return Stock.objects.all()
        return Stock.objects.filter(branch__shop__owner=user)
