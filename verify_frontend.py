
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.test import Client
from users.models import CustomUser

def verify_frontend():
    client = Client()
    print("Starting Frontend Verification...")

    # 1. Check Login Page
    print("\n[1] Accessing Login Page...")
    response = client.get('/accounts/login/')
    if response.status_code == 200:
        if "eDuka Login" in response.content.decode():
             print("Login Page verification successful (Title found).")
        else:
             print("Login Page loaded but title not found.")
    else:
        print(f"Failed to access login page: {response.status_code}")
        return

    # 2. Login
    print("\n[2] Logging In...")
    # Ensure user exists (using owner5 from previous run)
    try:
        user = CustomUser.objects.get(username='owner5')
        print(f"Found user: {user.username}")
    except CustomUser.DoesNotExist:
        print("User owner5 not found. Creating...")
        user = CustomUser.objects.create_user('owner5', 'owner5@example.com', 'password123', role='OWNER')

    login_success = client.login(username='owner5', password='password123')
    if login_success:
        print("Login Check: True")
    else:
        print("Login Check: False (Failed)")
        return

    # 3. Access Dashboard
    print("\n[3] Accessing Dashboard...")
    response = client.get('/', follow=True) # Following redirect from login if needed, or direct access
    
    if response.status_code == 200:
        content = response.content.decode()
        if "Dashboard" in content and "Total Sales" in content:
            print("Dashboard verification successful (Stats widgets found).")
        else:
            print("Dashboard loaded but expected content not found. Dumping snippet:")
            print(content[:500])
    else:
        print(f"Failed to access dashboard: {response.status_code}")

if __name__ == '__main__':
    verify_frontend()
