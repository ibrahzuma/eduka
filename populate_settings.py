import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from shops.models import Shop, ShopSettings
from django.contrib.auth import get_user_model

User = get_user_model()

# Get the first shop (assuming single user/shop for dev)
shop = Shop.objects.first()
if not shop:
    print("No shop found, creating one...")
    user = User.objects.first()
    if user:
        shop = Shop.objects.create(owner=user, name="Salama Shop")
    else:
        print("No user found to create shop.")
        exit()

# Update Shop Details
shop.name = "Salama Shop"
shop.address = "Mji Mpya, Ubungo, Dar es Salaam, Tanzania"
shop.website = "https://www.example.com"
shop.phone = "255747093762"
shop.email = "" # Prompt showed empty
shop.save()
print(f"Updated Shop: {shop.name}")

# Update Settings
settings, _ = ShopSettings.objects.get_or_create(shop=shop)
settings.plan = ShopSettings.Plan.DUKA # Or whatever matches "Duka"
# "Trial days left 6 Days"
# "Next billing date 21, Dec 2025"

# If they want "Trial days left: 6", that implies Plan is TRIAL?
# But display says "Pricing Plan: Duka".
# And "Trial days left 6 Days".
# Maybe it's a "Duka (Trial)" plan?
# Let's set Plan to TRIAL so the "Trial days left" badge shows up in my template logic.
settings.plan = ShopSettings.Plan.TRIAL

# Set trial end date to 6 days from now
settings.trial_ends_at = timezone.now() + datetime.timedelta(days=6)

# Set next billing date to Dec 21, 2025? (That's huge, maybe they mean 2023 or just +6 days?)
# Prompt: "21, Dec 2025"
# I will set strictly what they asked for next_billing_date.
try:
    target_date = datetime.datetime(2025, 12, 21, tzinfo=timezone.utc)
    settings.next_billing_date = target_date
except:
    settings.next_billing_date = timezone.now() + datetime.timedelta(days=6)

settings.billing_amount = 60000.00
settings.save()
print(f"Updated Settings for {shop.name}")
