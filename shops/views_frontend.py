from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ShopForm, BranchForm
from .models import Shop, Branch, ShopSettings
from django.contrib import messages

class ShopCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ShopForm()
        return render(request, 'shops/create.html', {'form': form})

    def post(self, request):
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            
            # Logic from API: Automatic Settings & Main Branch are handled via Signal or Manual?
            # API had it in Serializer. Let's do it here explicitly to be safe, 
            # or rely on the same logic if we extracted it. 
            # Looking at previous Serializer logic: 
            # "Branch.objects.create(shop=shop, name='Main Branch', location='HQ')"
            # "ShopSettings.objects.create(shop=shop)"
            
            # Let's verify if we have signals. I didn't create signals.
            # So I must replicate the startup logic here.
            
            ShopSettings.objects.get_or_create(shop=shop)
            Branch.objects.create(shop=shop, name='Main Branch', address='HQ')

            messages.success(request, f"Shop '{shop.name}' created successfully!")
            return redirect('dashboard')
        
        return render(request, 'shops/create.html', {'form': form})
class BranchListView(LoginRequiredMixin, View):
    def get(self, request):
        shop = None
        if getattr(request.user, 'shop', None):
            shop = request.user.shop
        elif hasattr(request.user, 'shops') and request.user.shops.exists():
            shop = request.user.shops.first()
        elif hasattr(request.user, 'employee_profile'):
            shop = request.user.employee_profile.shop
            
        if not shop:
             # Redirect to shop creation if no shop exists
             return redirect('shop_create')

        branches = Branch.objects.filter(shop=shop)
        form = BranchForm()
        return render(request, 'shops/branch_list.html', {'branches': branches, 'form': form, 'shop': shop})

    def post(self, request):
        shop = None
        if hasattr(request.user, 'shops') and request.user.shops.exists():
            shop = request.user.shops.first()
        elif hasattr(request.user, 'employee_profile'):
            shop = request.user.employee_profile.shop

        if not shop:
             messages.error(request, "No shop found.")
             return redirect('dashboard')

        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.shop = shop
            # Handle Single Main Branch logic optional: if new one is main, demote others?
            # For simplicity, we just save.
            branch.save()
            
            # AUTOMATICALLY INIT STOCK FOR THIS NEW BRANCH?
            # If we want products to be available here, we should create 0 stock entries for all existing products.
            from inventory.models import Product, Stock
            products = Product.objects.filter(shop=shop)
            stock_objects = [
                Stock(product=p, branch=branch, quantity=0) 
                for p in products
            ]
            Stock.objects.bulk_create(stock_objects)

            messages.success(request, "Branch created successfully!")
            return redirect('branch_list')
        
        branches = Branch.objects.filter(shop=shop)
        return render(request, 'shops/branch_list.html', {'branches': branches, 'form': form, 'shop': shop})

from django.utils import timezone

class ShopSettingsView(LoginRequiredMixin, View):
    template_name = 'shops/settings.html'

    def get_shop(self, request):
        if getattr(request.user, 'shop', None):
            return request.user.shop
        elif hasattr(request.user, 'shops') and request.user.shops.exists():
            return request.user.shops.first()
        elif hasattr(request.user, 'employee_profile'):
            return request.user.employee_profile.shop
        return None

    def get(self, request):
        shop = self.get_shop(request)
        if not shop:
            messages.error(request, "No shop found.")
            return redirect('shop_create')
            
        settings, _ = ShopSettings.objects.get_or_create(shop=shop)
        form = ShopForm(instance=shop)
        
        # Calculate Trial Days Left
        trial_days_left = 0
        if settings.plan == ShopSettings.Plan.TRIAL and settings.trial_ends_at:
            delta = settings.trial_ends_at - timezone.now()
            trial_days_left = max(0, delta.days)
        
        # Default mock data if missing for the demo view requested
        if not settings.next_billing_date:
             # Just for display as per request example "21, Dec 2025"
             import datetime
             settings.next_billing_date = timezone.now() + datetime.timedelta(days=6) # Mock
             settings.billing_amount = 60000
        
        context = {
            'shop': shop,
            'settings': settings,
            'form': form,
            'trial_days_left': trial_days_left
        }
        return render(request, self.template_name, context)

    def post(self, request):
        shop = self.get_shop(request)
        if not shop:
            return redirect('dashboard')
            
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, "Duka details updated successfully!")
            return redirect('settings')
            
        settings, _ = ShopSettings.objects.get_or_create(shop=shop)
        context = {
            'shop': shop,
            'settings': settings,
            'form': form
        }
        return render(request, self.template_name, context)
