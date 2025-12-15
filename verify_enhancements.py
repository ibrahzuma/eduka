
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.test import Client
from users.models import CustomUser

def verify_phone_login_and_design():
    client = Client()
    print("Starting Login/Design Verification...")
    
    # 1. Create User with Phone
    phone = '0712345678'
    username = 'phoneuser'
    password = 'password123'
    
    CustomUser.objects.filter(username=username).delete()
    user = CustomUser.objects.create_user(username=username, email='p@e.com', password=password, phone=phone)
    print(f"\n[1] User created: {username} | Phone: {phone}")

    # 2. Test Login with Username (Standard)
    login_success = client.login(username=username, password=password)
    print(f"Login with Username: {login_success}")
    client.logout()

    # 3. Test Login with Phone (New Backend)
    # The standard client.login() uses the KEYWORD arguments to pass to authenticate().
    # Our backend looks for 'username' kwarg but checks against phone field too.
    # So we pass phone as 'username'.
    login_success_phone = client.login(username=phone, password=password)
    print(f"Login with Phone: {login_success_phone}")
    
    if login_success_phone:
        print("Phone Authentication: SUCCESS")
    else:
        print("Phone Authentication: FAILED")

    # 4. Check Registration Page Design Elements (Static Check)
    print("\n[2] Checking Register Page Design...")
    response = client.get('/accounts/register/')
    content = response.content.decode()
    
    if "btn-super-cool" in content:
        print("Design Check: 'btn-super-cool' class found.")
    else:
        print("Design Check: 'btn-super-cool' NOT found.")
        
    if "Dodoma" in content and "Zanzibar" in content:
        print("Region Check: New regions (Dodoma, Zanzibar) found.")
    else:
        print("Region Check: New regions NOT found.")

if __name__ == '__main__':
    verify_phone_login_and_design()
