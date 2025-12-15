from rest_framework import viewsets, permissions
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return Customer.objects.all()
        return Customer.objects.filter(shop__owner=user)
