import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from users.forms import EmployeeForm
from django.contrib.auth import get_user_model
from users.models import Role

User = get_user_model()

def verify_form_fields():
    print(">>> Verifying EmployeeForm Fields...")
    form = EmployeeForm()
    fields = form.fields.keys()
    print(f"Fields found: {list(fields)}")
    
    expected_fields = ['username', 'email', 'phone', 'assigned_role', 'branch', 'password']
    for field in expected_fields:
        if field not in fields:
            print(f"FAILED: Missing field '{field}'")
            return
    if 'first_name' in fields or 'last_name' in fields:
        print("FAILED: first_name or last_name should NOT be present.")
        return
    print("SUCCESS: All expected fields are present.")

    print("\n>>> Verifying Save...")
    role, _ = Role.objects.get_or_create(name='TestRole')
    data = {
        'username': 'testuser_simple',
        'email': 'test@example.com',
        'phone': '1234567890',
        'assigned_role': role.id,
        'password': 'password123'
    }
    
    if User.objects.filter(username='testuser_simple').exists():
         User.objects.filter(username='testuser_simple').delete()
         
    form = EmployeeForm(data=data)
    if form.is_valid():
        user = form.save()
        print(f"User Created: {user.username}")
        assert user.username == 'testuser_simple'
        # assert user.first_name == '' # Should be empty
        assert user.check_password('password123')
        print("SUCCESS: User saved correctly.")
        user.delete()
    else:
        print(f"FAILED: Form Invalid: {form.errors}")

if __name__ == '__main__':
    verify_form_fields()
