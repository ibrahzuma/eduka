import os
import sys
import django
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from dashboard.views import DashboardTemplateView

User = get_user_model()

print("--- DIAGNOSTIC START ---")

try:
    # 1. Get a test user
    user = User.objects.first()
    if not user:
        print("ERROR: No users found in database.")
        sys.exit(1)
        
    print(f"Testing with user: {user.username} (ID: {user.id})")
    
    # 2. Simulate Request
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request.user = user
    
    # 3. Instantiate View
    view = DashboardTemplateView()
    view.request = request
    
    print("Executing get_context_data()...")
    context = view.get_context_data()
    
    print("--- SUCCESS ---")
    print("Context keys generated:", context.keys())
    print("Subscription Status:", context.get('subscription_status'))
    print("Days Left:", context.get('days_left'))
    
except Exception as e:
    print("\n--- CRASH DETECTED ---")
    import traceback
    traceback.print_exc()

print("--- DIAGNOSTIC END ---")
