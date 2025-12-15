from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import PurchaseOrder, Supplier
from .forms import PurchaseOrderForm, SupplierForm
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView

class BaseShopView(LoginRequiredMixin):
    def get_shop(self):
        if hasattr(self.request.user, 'shops') and self.request.user.shops.exists():
            return self.request.user.shops.first()
        elif hasattr(self.request.user, 'employee_profile'):
             return self.request.user.employee_profile.shop
        return None

class SupplierListView(BaseShopView, ListView):
    model = Supplier
    template_name = 'purchase/supplier_list.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return Supplier.objects.filter(shop=shop).order_by('name')
        return Supplier.objects.none()

class SupplierCreateView(BaseShopView, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchase/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    def form_valid(self, form):
        shop = self.get_shop()
        if not shop:
             messages.error(self.request, "No shop associated.")
             return self.form_invalid(form)
        form.instance.shop = shop
        messages.success(self.request, "Supplier added successfully!")
        return super().form_valid(form)

class SupplierUpdateView(BaseShopView, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchase/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    def get_queryset(self):
        # Ensure user can only edit their own shop's suppliers
        shop = self.get_shop()
        if shop:
            return Supplier.objects.filter(shop=shop)
        return Supplier.objects.none()

class SupplierDetailView(BaseShopView, DetailView):
    model = Supplier
    template_name = 'purchase/supplier_detail.html'
    context_object_name = 'supplier'

    def get_queryset(self):
         shop = self.get_shop()
         return Supplier.objects.filter(shop=shop) if shop else Supplier.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add purchase history
        context['recent_purchases'] = PurchaseOrder.objects.filter(
            supplier=self.object
        ).order_by('-created_at')[:10]
        return context

class BaseShopView(LoginRequiredMixin):
    def get_shop(self):
        if hasattr(self.request.user, 'shops') and self.request.user.shops.exists():
            return self.request.user.shops.first()
        elif hasattr(self.request.user, 'employee_profile'):
             return self.request.user.employee_profile.shop
        return None

class PurchaseListView(BaseShopView, ListView):
    model = PurchaseOrder
    template_name = 'purchase/purchase_list.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return PurchaseOrder.objects.filter(shop=shop).order_by('-created_at')
        return PurchaseOrder.objects.none()

class PurchaseCreateView(BaseShopView, CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchase/purchase_form.html'
    success_url = reverse_lazy('purchase_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['shop'] = self.get_shop()
        return kwargs

    def form_valid(self, form):
        shop = self.get_shop()
        if not shop:
             messages.error(self.request, "No shop associated.")
             return self.form_invalid(form)
        
        form.instance.shop = shop
        # Default to first branch logic for now
        if hasattr(shop, 'branches') and shop.branches.exists():
            form.instance.branch = shop.branches.first()
            
        messages.success(self.request, "Purchase Order created successfully!")
        return super().form_valid(form)

class PurchaseRecentView(BaseShopView, ListView):
    model = PurchaseOrder
    template_name = 'purchase/purchase_list.html'
    context_object_name = 'purchases'
    
    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return PurchaseOrder.objects.filter(shop=shop).order_by('-created_at')[:5]
        return PurchaseOrder.objects.none()

class PlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/placeholder.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.path.strip('/').replace('/', ' ').title()
        return context
