from django.db.models.signals import post_save
from django.dispatch import receiver
from shops.models import Shop
from .models import ShopSubscription, SubscriptionPlan
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=Shop)
def create_shop_subscription(sender, instance, created, **kwargs):
    if created:
        # Get or Create a 'Trial' Plan
        trial_plan, _ = SubscriptionPlan.objects.get_or_create(
            slug='trial',
            defaults={
                'name': 'Free Trial',
                'description': '7-Day Free Trial',
                'price_monthly': 0.00
            }
        )
        
        # Create Subscription
        ShopSubscription.objects.create(
            shop=instance,
            plan=trial_plan,
            status='TRIAL',
            billing_cycle='WEEKLY',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7)
        )
