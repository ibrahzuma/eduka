import os
import sys
import django
import traceback

# 1. Setup Django Environment
# Robust checking for dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded .env file")
except ImportError:
    print("Warning: python-dotenv not installed. Relying on system environment variables.")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')

try:
    django.setup()
except Exception as e:
    print(f"CRITICAL: Django setup failed: {e}")
    traceback.print_exc()
    sys.exit(1)

from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from dashboard.views import DashboardTemplateView

User = get_user_model()

def run_diagnostic():
    print("\n--- DIAGNOSTIC START ---")
    
    # 2. Get Test User
    user = User.objects.filter(is_superuser=False).first()
    if not user:
        print("Notice: No standard user found. Trying superuser.")
        user = User.objects.filter(is_superuser=True).first()
    
    if not user:
        print("ERROR: No users found in database!")
        return

    print(f"Testing with User: {user.username} (Superuser: {user.is_superuser})")

    # 3. Simulate Request
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request.user = user

    # 4. Execute View Logic
    print("\n[Executing View Logic]")
    try:
        view = DashboardTemplateView()
        view.setup(request)
        
        # Test get_context_data explicitly
        context = view.get_context_data()
        print("Context Generated Successfully.")
        
        # Check specific keys
        print(f"show_subscription_banner: {context.get('show_subscription_banner', 'MISSING')}")
        print(f"subscription_status: {context.get('subscription_status')}")
        
    except Exception as e:
        print(f"VIEW ERROR: {e}")
        traceback.print_exc()
        return

    # 5. Execute Template Rendering (The likely crash point)
    print("\n[Rendering Template]")
    try:
        client = Client()
        client.force_login(user)
        response = client.get('/dashboard/')
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 500:
            print("SERVER ERROR (500) DETECTED!")
            # Django's test client usually swallows the exception details in the response
            # But we can try to render the response content which might have debug info if DEBUG=True
            # Or we can rely on the View logic test above if it was Logic error.
            # If it's TemplateSyntaxError, client.get might assume it handles it.
            
    except Exception as e:
        print(f"TEMPLATE RENDER ERROR: {e}")
        traceback.print_exc()

    print("--- DIAGNOSTIC END ---")

if __name__ == '__main__':
    run_diagnostic()
