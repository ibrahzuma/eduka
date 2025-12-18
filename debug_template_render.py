import os
import django
from django.conf import settings
from django.template import Context, Template
from django.template.loader import get_template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from users.models import CustomUser, Role
from django.test import RequestFactory

class MockRole:
    def __init__(self, perms):
        self.permissions = perms

class MockUser:
    def __init__(self, role_name, perms):
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.role = role_name
        self.is_authenticated = True
        self.is_superuser = False
        self.assigned_role = MockRole(perms) if role_name == 'EMPLOYEE' else None

    def get_role_display(self):
        return self.role

def test_render():
    print(">>> Testing base.html Render Logic")
    
    # 1. Setup Mock User with Sales access only
    # Finance should be LOCKED
    user = MockUser('EMPLOYEE', {'sales': ['view']})
    
    request = RequestFactory().get('/')
    request.user = user
    
    # 2. Render base.html using get_template
    # This ensures standard loading pipeline
    t = get_template('base.html')
    # render accepts a dict or Context. For get_template (backend template), dict is preferred.
    # request is needed for permission_tags (takes_context=True usually needs context processor or manual pass)
    # Our permission_tags use 'user' mainly, but has_permission uses context['request']. logic:
    # can_view filter uses 'user' argument. So request is not strictly needed for 'can_view', 
    # but 'base.html' might use request.path using context processors. 
    # We must pass 'request' in context.
    
    ctx = {'user': user, 'request': request}
    rendered = t.render(ctx)
    
    print(f"Rendered Length: {len(rendered)}")
    
    with open('debug_rendered.html', 'w', encoding='utf-8') as f:
        f.write(rendered)
    print("Dumped rendered HTML to debug_rendered.html")
    
    # 3. Check Sales (Should be Active)
    if 'data-bs-target="#collapseSales"' in rendered:
        print("[PASS] Sales is ACTIVE (Dropdown found)")
    else:
        print("[FAIL] Sales is LOCKED or Missing")
        
    # 4. Check Finance (Should be Locked)
    if 'Finance' in rendered:
        print("[PASS] Finance link found")
        if 'data-bs-target="#collapseFinance"' not in rendered:
             print("[PASS] Finance is LOCKED (No dropdown)")
        else:
             print("[FAIL] Finance is ACTIVE (Unexpected dropdown!)")
    else:
        print("[FAIL] Finance link NOT FOUND")

if __name__ == '__main__':
    test_render()
