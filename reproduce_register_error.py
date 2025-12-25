
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.test import RequestFactory
# from django.contrib.auth.models import AnonymousUser # Not needed
from users.views_frontend import RegisterView
from dashboard.views import DashboardTemplateView
from users.forms import UserRegistrationForm
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

def reproduce_error():
    print("Reproducing Registration -> Dashboard 500 Error...")
    
    # 1. Simulate Registration POST
    factory = RequestFactory()
    
    # Unique user data
    timestamp = int(timezone.now().timestamp())
    username = f"newuser_{timestamp}"
    email = f"newuser_{timestamp}@test.com"
    data = {
        'username': username,
        'email': email,
        'password': 'password123',
        'confirm_password': 'password123',
        'first_name': 'New',
        'last_name': 'User',
        'phone': f"07{timestamp % 100000000:08d}", # unique phone
        'business_name': f"My Business {timestamp}",
        'region': 'Dar es Salaam',
        'district': 'Ilala',
        'street': 'Upanga',
    }
    
    print(f"Registering user: {username}")
    
    # Manually Create User & Shop to mimic RegisterView logic if we don't want to run the full view stack
    # But running the view is better to catch everything.
    # However, RegisterView needs a request with session/messages.
    
    from users.models import CustomUser
    
    # Let's just manually do what RegisterView does, to control the state exactly
    try:
        user = CustomUser.objects.create_user(username=username, email=email, password='password123')
        user.first_name = 'New'
        user.last_name = 'User'
        user.role = 'OWNER'
        user.save()
        
        from shops.models import Shop, Branch, ShopSettings
        shop = Shop.objects.create(owner=user, name=data['business_name'])
        ShopSettings.objects.create(shop=shop)
        Branch.objects.create(shop=shop, name='Main Branch', address="DSM", is_main=True)
        
        print(f"User {user.username} created with Shop {shop.name}")
        
    except Exception as e:
        print(f"Registration simulation failed: {e}")
        return

    # 2. Simulate Dashboard Access
    print("Accessing Dashboard...")
    request = factory.get('/dashboard/')
    request.user = user
    
    # Add session/messages support to request
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    messages = MessageMiddleware(lambda x: None)
    messages.process_request(request)
    
    view = DashboardTemplateView.as_view()
    
    try:
        response = view(request)
        if response.status_code == 200:
            print("SUCCESS: Dashboard accessed successfully.")
            # Render to catch template errors
            if hasattr(response, 'render'):
                 response.render()
            print("Rendered successfully.")
        else:
            print(f"FAILURE: Status Code {response.status_code}")
    except Exception as e:
        print("CRITICAL FAILURE: 500 Error Caught!")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    reproduce_error()
