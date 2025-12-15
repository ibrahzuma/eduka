
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.test import Client
from users.models import CustomUser

def verify_registration_flow():
    client = Client()
    print("Starting Registration Verification...")

    # 1. Access Register Page
    print("\n[1] Accessing Register Page...")
    response = client.get('/accounts/register/')
    if response.status_code == 200:
        if "Create eDuka Account" in response.content.decode():
             print("Register Page verification successful.")
        else:
             print("Register Page loaded but content missing.")
    else:
        print(f"Failed to access register page: {response.status_code}")
        return

    # 2. Submit Registration
    print("\n[2] Submitting Registration Form...")
    new_user_data = {
        'username': 'newowner2',
        'email': 'new2@example.com',
        'phone': '0700000002',
        'business_name': 'New Shop Auto',
        'business_type': 'Retail',
        'region': 'Dar es Salaam',
        'district': 'Ilala', # Note: Cleaned data might require valid choice if Choices were strictly enforced in form but not HTML. Text is fine for now if simple CharField or valid choice. Default form uses ChoiceField for region but CharField for district? Wait, form definition used CharField for district with empty choices. Will it validate?
        'street': 'Posta',
        'password': 'password123',
        'confirm_password': 'password123'
    }
    
    # Ensure user doesn't exist
    CustomUser.objects.filter(username='newowner2').delete()

    response = client.post('/accounts/register/', new_user_data, follow=True)
    
    # Check if redirected to dashboard
    if response.redirect_chain:
        last_url, status = response.redirect_chain[-1]
        print(f"Redirected to: {last_url} (Status: {status})")
        if last_url == '/' or last_url.endswith('?next=/'): # Dashboard URL
             print("Registration Successful: Redirected to Dashboard.")
        else:
             print("Registration Warning: Redirected to unexpected URL.")
    else:
        print(f"Registration Failed (No Redirect). Status: {response.status_code}")
        if 'form' in response.context:
             print(f"Form Errors: {response.context['form'].errors}")

    # 3. Verify Database
    if CustomUser.objects.filter(username='newowner2').exists():
        print("Database Verification: User 'newowner2' exists.")
    else:
        print("Database Verification: User 'newowner2' NOT found.")

if __name__ == '__main__':
    verify_registration_flow()
