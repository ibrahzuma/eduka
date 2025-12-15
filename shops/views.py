from rest_framework import viewsets, permissions
from .models import Shop, Branch, ShopSettings
from .serializers import ShopSerializer, BranchSerializer, ShopSettingsSerializer

class ShopViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShopSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return Shop.objects.all()
        return Shop.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BranchViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BranchSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return Branch.objects.all()
        return Branch.objects.filter(shop__owner=user)

class ShopSettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShopSettingsSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return ShopSettings.objects.all()
        return ShopSettings.objects.filter(shop__owner=user)
