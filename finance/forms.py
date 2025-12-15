from django import forms
from .models import Expense, Income
from shops.models import Branch

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date', 'branch']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rent, Utilities'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expense details'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)
        if shop:
            self.fields['branch'].queryset = Branch.objects.filter(shop=shop)

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'description', 'amount', 'date', 'branch']
        widgets = {
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Consulting, Service'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Details (optional)'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)
        if shop:
            self.fields['branch'].queryset = Branch.objects.filter(shop=shop)
