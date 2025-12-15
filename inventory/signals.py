from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Stock
from shops.models import Branch

@receiver(post_save, sender=Product)
def create_initial_stock(sender, instance, created, **kwargs):
    """
    When a new product is created, automatically create Stock entries
    with 0 quantity for all branches in the product's shop.
    """
    if created:
        shop = instance.shop
        branches = Branch.objects.filter(shop=shop)
        for branch in branches:
            Stock.objects.get_or_create(
                product=instance,
                branch=branch,
                defaults={'quantity': 0}
            )
