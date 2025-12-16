from django.utils import timezone
from shops.models import Shop

def subscription_status(request):
    """
    Context processor to make 'subscription_is_valid' available in all templates.
    """
    if not request.user.is_authenticated:
        return {'subscription_is_valid': False}

    # Superusers always have access
    if request.user.is_superuser:
        return {'subscription_is_valid': True}

    # Check User's Shop
    try:
        shop = Shop.objects.filter(owner=request.user).first()
        if shop:
            # 1. Check DB Subscription
            if hasattr(shop, 'subscription') and shop.subscription.is_valid():
                return {'subscription_is_valid': True}
            
            # 2. Check Trial (7 Days)
            days_since_reg = (timezone.now() - shop.created_at).days
            if days_since_reg < 7:
                return {'subscription_is_valid': True}
                
    except Exception:
        pass

    return {'subscription_is_valid': False}
