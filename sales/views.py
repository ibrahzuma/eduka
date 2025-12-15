from rest_framework import viewsets, permissions
from .models import Sale
from .serializers import SaleSerializer

class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SaleSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return Sale.objects.all()
        return Sale.objects.filter(shop__owner=user)
