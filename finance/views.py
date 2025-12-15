from rest_framework import viewsets, permissions
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'SUPER_ADMIN' or user.is_superuser:
            return Expense.objects.all()
        return Expense.objects.filter(shop__owner=user)
