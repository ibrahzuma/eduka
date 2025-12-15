from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from shops.models import Shop
from .models import ShopSubscription

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Skip for Superusers
        if request.user.is_superuser:
            return self.get_response(request)

        # Explicitly Allowed Paths (Dashboard, Payment, Logout, Static)
        allowed_paths = [
            reverse('dashboard:home'),
            reverse('pricing_plans'), 
            '/subscriptions/', # Allow all subscription/payment URLs
            '/admin/',
            '/static/',
            '/media/',
            '/api/', # Allow API for now, or secure it separately
            '/accounts/logout/'
        ]
        
        if any(request.path.startswith(path) for path in allowed_paths):
            return self.get_response(request)

        # Check User's Shop Subscription
        # Assuming user has one shop for now or checking the first one
        # Ideally, we check the shop in the session or context
        try:
            shop = Shop.objects.filter(owner=request.user).first()
            if shop:
                # Ensure subscription exists (Signal should have created it, but just in case)
                if not hasattr(shop, 'subscription'):
                    # Fallback: Redirect to pricing or create trial?
                    return redirect('pricing_plans')

                sub = shop.subscription
                
                # Check Validity
                if not sub.is_valid():
                     # Expired! Redirect to Pricing
                     return redirect('pricing_plans')
                     
        except Exception as e:
            # Log error
            pass

        return self.get_response(request)
