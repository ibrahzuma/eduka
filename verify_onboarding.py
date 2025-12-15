
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.test import Client
from users.models import CustomUser
from shops.models import Shop

def verify_onboarding():
    client = Client()
    print("Starting Onboarding Verification...")
    
    # 1. Login as newowner1 (created in previous step)
    print("\n[1] Logging in as 'newowner1'...")
    try:
        user = CustomUser.objects.get(username='newowner1')
    except CustomUser.DoesNotExist:
        print("User 'newowner1' not found. Please run verify_registration.py first.")
        return

    client.force_login(user)
    
    # 2. Check Dashboard for "Create Shop" Prompt
    print("\n[2] Checking Dashboard for Prompt...")
    response = client.get('/')
    content = response.content.decode()
    if "Create My Shop" in content:
        print("Dashboard Verification: 'Create My Shop' button found.")
    else:
        print("Dashboard Warning: 'Create My Shop' button NOT found.")
        # If user already has a shop from previous attempts, this might be why.
        print(f"Total Shops detected: {Shop.objects.filter(owner=user).count()}")

    # 3. Create Shop
    print("\n[3] Creating Shop via Frontend...")
    shop_data = {
        'name': 'New User Shop',
        # logo optional
    }
    response = client.post('/shops/create/', shop_data, follow=True)
    
    if response.status_code == 200:
        if "Shop &#x27;New User Shop&#x27; created successfully!" in response.content.decode() or \
           "Shop 'New User Shop' created successfully!" in response.content.decode():
             print("Shop Creation Successful: Success message found.")
        else:
             # Check if redirected to dashboard
             if response.redirect_chain and response.redirect_chain[-1][0] == '/':
                 print("Shop Creation: Redirected to Dashboard.")
             else:
                 print(f"Shop Creation Warning: Status {response.status_code}")
    else:
        print(f"Shop Creation Failed: {response.status_code}")

    # 4. Verify Database
    if Shop.objects.filter(owner=user, name='New User Shop').exists():
        print("Database Verification: 'New User Shop' exists.")
    else:
        print("Database Verification: Shop NOT found.")

if __name__ == '__main__':
    verify_onboarding()
