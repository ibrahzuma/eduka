from django import forms
from .models import Product, Category
from shops.models import Branch

class ProductForm(forms.ModelForm):
    # Extra fields for stock initialization
    opening_stock = forms.IntegerField(
        required=False, initial=0, 
        label="Opening Stock (Idadi ya stock iliyopo)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
    )
    low_stock_threshold = forms.IntegerField(
        required=False, initial=0, 
        label="Minimum Threshold (Kiwango cha chini cha stock)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
    )

    class Meta:
        model = Product
        fields = ['product_type', 'name', 'category', 'sku', 'si_unit', 'selling_price', 'cost_price', 'image']
        labels = {
            'product_type': 'Product (Bidhaa) or Service (Huduma) ?',
            'name': 'Product Name (Jina la bidhaa)',
            'category': 'Category (Kundi la bidhaa)',
            'sku': 'SKU (Code ya bidhaa)',
            'si_unit': 'SI Unit (Kipimo mf. Kilo, Dozen, n.k)',
            'selling_price': 'Selling Price(Bei ya Kuuzia) (Tshs)',
            'cost_price': 'Buying Price (Bei Ya Kununulia)',
            'image': 'Product Image (Picha ya bidhaa)'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vinywaji'}), # User asked "Vinywaji" as placeholder/example
            'category': forms.Select(attrs={'class': 'form-select display-block w-100'}),
            'product_type': forms.Select(attrs={'class': 'form-select'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'si_unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pcs, Kilo...'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if shop:
            self.fields['category'].queryset = Category.objects.filter(shop=shop)
        else:
            self.fields['category'].queryset = Category.objects.none()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description (Optional)'}),
        }

class StockAdjustmentForm(forms.Form):
    ADJUSTMENT_TYPES = [
        ('ADD', 'Add Stock (+)'),
        ('REDUCE', 'Reduce Stock (-)'),
        ('SET', 'Set Exact Quantity (=)'),
    ]
    
    stock_id = forms.IntegerField(widget=forms.HiddenInput())
    adjustment_type = forms.ChoiceField(
        choices=ADJUSTMENT_TYPES, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity = forms.IntegerField(
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'})
    )
    reason = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason (e.g., Restock, Damaged)'})
    )

class StockTransferForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'})
    )
    source_branch = forms.ModelChoiceField(
        queryset=Branch.objects.none(),
        label="Source Branch (Toa hapa)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    destination_branch = forms.ModelChoiceField(
        queryset=Branch.objects.none(),
         label="Destination Branch (Peleka hapa)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'})
    )
    note = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for transfer'})
    )

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super(StockTransferForm, self).__init__(*args, **kwargs)
        if shop:
            self.fields['product'].queryset = Product.objects.filter(shop=shop, product_type=Product.Type.GOODS)
            self.fields['source_branch'].queryset = Branch.objects.filter(shop=shop)
            self.fields['destination_branch'].queryset = Branch.objects.filter(shop=shop)

class PurchaseForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'})
    )
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.none(),
        label="Branch (Tawi la kupokelea)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'})
    )
    cost_price = forms.DecimalField(
        min_value=0,
        required=False,
        label="New Cost Price (Bei Mpya ya Kununua - Optional)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Leave empty to keep current'})
    )
    # Optional fields for logging
    supplier = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'})
    )
    reference_number = forms.CharField(
        required=False,
        label="Reference / Invoice No.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ref No.'})
    )
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes'})
    )

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super(PurchaseForm, self).__init__(*args, **kwargs)
        if shop:
            self.fields['product'].queryset = Product.objects.filter(shop=shop, product_type=Product.Type.GOODS)
            self.fields['branch'].queryset = Branch.objects.filter(shop=shop)
