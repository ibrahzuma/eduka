import os
import sys
import django
import traceback

# Setup
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')

try:
    django.setup()
except Exception as e:
    print(f"Setup Error: {e}")
    sys.exit(1)

from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.loader import render_to_string
from dashboard.views import SuperUserUserListView

User = get_user_model()

def run_test():
    print("--- DIAGNOSTIC: User Management ---")
    
    # 1. Get Superuser
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("CRITICAL: No Superuser found to test with.")
        return

    print(f"Testing as: {admin.username}")

    # 2. Test URL Resolution
    print("\n[Testing URL Resolution]")
    try:
        url = reverse('superuser_user_list')
        print(f"List URL: {url} [OK]")
        
        # Test Delete URL for admin itself
        del_url = reverse('superuser_user_delete', args=[admin.pk])
        print(f"Delete URL (test): {del_url} [OK]")
    except Exception as e:
        print(f"URL ERROR: {e}")
        traceback.print_exc()

    # 3. Test View Context
    print("\n[Testing View Context]")
    factory = RequestFactory()
    request = factory.get(reverse('superuser_user_list'))
    request.user = admin
    
    try:
        view = SuperUserUserListView()
        view.setup(request)
        context = view.get_context_data()
        users = context['users']
        print(f"Context fetched. Users count: {users.count()}")
    except Exception as e:
        print(f"VIEW CONTEXT ERROR: {e}")
        traceback.print_exc()
        return

    # 4. Test Template Rendering
    print("\n[Testing Template Loop]")
    try:
        # We manually render to catch exact loop failure
        for u in users:
            try:
                # Test logic inside loop
                # Check relation
                has_shops = u.shops.exists() if hasattr(u, 'shops') else False
                # Check URL generation
                del_link = reverse('superuser_user_delete', args=[u.pk])
            except Exception as loop_e:
                print(f"ERROR on user {u.username} (ID: {u.id}): {loop_e}")
                traceback.print_exc()

        # Full Render
        print("Rendering full template...")
        content = render_to_string('dashboard/superuser_users_list.html', context, request)
        print("Template Render: SUCCESS")
        
    except Exception as e:
        print(f"TEMPLATE RENDER ERROR: {e}")
        traceback.print_exc()

    print("--- DIAGNOSTIC END ---")

if __name__ == '__main__':
    run_test()
