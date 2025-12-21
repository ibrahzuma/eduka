import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from subscriptions.models import SubscriptionPlan

User = get_user_model()

def verify_plans_api():
    # Ensure user exists
    user = User.objects.filter(username='admin').first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    client = APIClient()
    client.force_authenticate(user=user)

    print("Fetching Plans...")
    response = client.get('/subscriptions/api/plans/')
    
    if response.status_code == 200:
        print("[PASS] API returned 200 OK")
        data = response.json()
        print(f"Found {len(data)} plans:")
        for plan in data:
            print(f"- {plan['name']} ({plan['cycle']}): {plan['display_price']}")
    else:
        print(f"[FAIL] API Status: {response.status_code}")
        print(response.content)

if __name__ == "__main__":
    verify_plans_api()
