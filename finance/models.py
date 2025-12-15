from django.db import models
from shops.models import Shop, Branch

class Expense(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='expenses')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=100) # e.g., Rent, Utilities, Salary
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

class Income(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='incomes')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='incomes')
    source = models.CharField(max_length=100) # e.g. Consulting, Service, Grant
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source}: {self.description} - {self.amount}"
