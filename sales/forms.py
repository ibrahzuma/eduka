from django import forms
from .models import SaleReturn, Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'payment_method']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Select Customer'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)
        if shop:
            from customers.models import Customer
            self.fields['customer'].queryset = Customer.objects.filter(shop=shop)

class SaleReturnForm(forms.ModelForm):
    class Meta:
        model = SaleReturn
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for return...'}),
        }

class SaleSearchForm(forms.Form):
    sale_id = forms.IntegerField(
        label='Sale ID', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sale ID (e.g. 104)'})
    )
