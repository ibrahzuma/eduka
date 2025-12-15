from django.urls import path
from .views_frontend import (
    ExpenseListView, ExpenseCreateView, 
    IncomeListView, IncomeCreateView
)

urlpatterns = [
    path('list/', ExpenseListView.as_view(), name='expense_list'),
    path('create/', ExpenseCreateView.as_view(), name='expense_create'),
    path('income/', IncomeListView.as_view(), name='income_list'),
    path('income/create/', IncomeCreateView.as_view(), name='income_create'),
]
