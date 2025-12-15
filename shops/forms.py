from django import forms
from .models import Shop, Branch

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'address', 'website', 'phone', 'email', 'logo']
        labels = {
            'name': 'Duka Name',
            'address': 'Duka Address',
            'website': 'Duka Website',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'logo': 'Duka Logo',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salama Shop'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Mji Mpya, Ubungo, Dar es Salaam, Tanzania'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'www.example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '255747093762'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'phone', 'is_main']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch Name (e.g. Kariakoo Branch)'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location/Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
