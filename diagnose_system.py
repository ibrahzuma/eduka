import os
import sys
import django
from django.conf import settings
import traceback

print("--- EDUKA BACKEND DIAGNOSTIC TOOL ---")
print(f"Python: {sys.version}")
print(f"CWD: {os.getcwd()}")

# 1. Setup Django
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
    django.setup()
    print("SUCCESS: Django setup complete.")
except Exception as e:
    print("FAILED: Django setup failed.")
    traceback.print_exc()
    sys.exit(1)

# 2. Check Static Files
print("\n--- 2. Checking Static Files ---")
try:
    storage = settings.STATICFILES_STORAGE
    root = settings.STATIC_ROOT
    print(f"Storage: {storage}")
    print(f"Root: {root}")
    if not os.path.exists(root):
        print("WARNING: STATIC_ROOT does not exist!")
    else:
        print(f"STATIC_ROOT exists. Items: {len(os.listdir(root))}")
        
    # Check for Manifest if using ManifestStorage
    if 'Manifest' in storage:
        manifest = os.path.join(root, 'staticfiles.json')
        if os.path.exists(manifest):
            print("SUCCESS: Manifest file found.")
        else:
            print("CRITICAL FAILURE: Manifest file MISSING. This WILL cause 500 Error.")
except Exception as e:
    print(f"Error checking static files: {e}")

# 3. Database & Models
print("\n--- 3. Checking Database Integrity ---")
from django.contrib.auth import get_user_model
from shops.models import Shop
User = get_user_model()

try:
    user_count = User.objects.count()
    shop_count = Shop.objects.count()
    print(f"Users: {user_count}")
    print(f"Shops: {shop_count}")
    
    # Check for Shops with NO owner
    orphans = Shop.objects.filter(owner__isnull=True).count()
    if orphans > 0:
        print(f"WARNING: Found {orphans} orphaned shops (No Owner).")
        
    # Check for Shops with NO Subscription (if Logic depends on it)
    try:
        shops_no_sub = Shop.objects.filter(subscription__isnull=True).count()
        print(f"Shops without Subscription: {shops_no_sub}")
    except Exception as e:
        print(f"Error checking subscriptions: {e}")

except Exception as e:
    print(f"Database Check Failed: {e}")

# 4. Middleware Simulation (Request Cycle)
print("\n--- 4. Simulating Full Request Cycle (Client) ---")
from django.test import Client
from django.urls import reverse

client = Client()

def test_url(name, user_obj=None):
    print(f"\nTesting URL Name: '{name}' ...")
    try:
        url = reverse(name)
        print(f"Resolved URL: {url}")
        if user_obj:
            client.force_login(user_obj)
        
        resp = client.get(url)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 500:
            print("!!! SERVER ERROR 500 DETECTED !!!")
            # Try to get more info if possible (though 500 blocks rendering)
        elif resp.status_code == 302:
            print(f"Redirects to: {resp.url}")
        else:
            print("OK")
    except Exception as e:
        print(f"CRASH: {e}")
        traceback.print_exc()

# Get a test user (Owner)
try:
    owner = User.objects.filter(role='OWNER').first()
    if not owner:
        print("Creating Mock Owner...")
        owner = User.objects.create_user('diag_owner', 'diag@test.com', 'pass', role='OWNER')
        Shop.objects.create(owner=owner, name="Diag Shop", slug="diag-shop")
    
    print(f"Using User: {owner}")
    
    # Test Dashboard
    test_url('dashboard', owner)
    
    # Test Pricing
    test_url('shop_pricing', owner)
    
    # Test Accounts Login (Anonymous)
    test_url('account_login', None)

except Exception as e:
    print(f"User setup failed: {e}")

print("\n--- DIAGNOSIS COMPLETE ---")
