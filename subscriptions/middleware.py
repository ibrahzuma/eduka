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

        # Explicitly Allowed Paths (Whitelist)
        # We allow the dashboard so users can see the 'Expired' banner and navigate to pricing
        allowed_paths = [
            reverse('dashboard'),        # Main Dashboard (Banner is here)
            reverse('shop_pricing'),     # Pricing Page
            '/subscriptions/',           # Payment processing
            '/admin/',                   # Admin panel
            '/static/',                  # Assets
            '/media/',                   # Media
            '/accounts/',                # Auth (Login/Logout/Password Reset)
            '/api/auth/',                # login/register is public
            '/api/pricing/',             # pricing is public
            '/api/donations/',           # donations usually public
        ]
        
        # Check if current path is allowed
        if any(request.path.startswith(path) for path in allowed_paths):
            return self.get_response(request)

        # Check User's Shop Subscription
        try:
            shop = Shop.objects.filter(owner=request.user).first()
            if shop:
                # 1. Check if DB Subscription exists and is valid
                if hasattr(shop, 'subscription') and shop.subscription.is_valid():
                    return self.get_response(request)
                
                # 2. Fallback: Registration Date Trial Logic
                # If no valid subscription, check if they are within 7 days of registration
                days_since_reg = (timezone.now() - shop.created_at).days
                if days_since_reg < 7:
                    # Grant Trial Access
                    return self.get_response(request)
                
                # 3. If neither valid sub nor trial -> BLOCK
                # Redirect to pricing page
                return redirect('shop_pricing')
                
        except Exception:
            # Safer to allow access if error occurs to avoid total lockout during bugs
            pass

        return self.get_response(request)
