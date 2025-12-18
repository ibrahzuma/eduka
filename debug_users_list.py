import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def list_employees():
    print("--- User Diagnostics ---")
    employees = User.objects.filter(role='EMPLOYEE')
    count = employees.count()
    print(f"Total Employees found: {count}")
    
    if count == 0:
        print("WARNING: No employees found in the database!")
        return

    print(f"{'Username':<20} | {'Phone':<15} | {'Email':<25} | {'Active':<6} | {'Has Password'}")
    print("-" * 90)
    
    for user in employees:
        has_pass = user.password.startswith('pbkdf2_')
        print(f"{user.username:<20} | {str(user.phone):<15} | {user.email:<25} | {str(user.is_active):<6} | {has_pass}")
        
    print("-" * 90)
    print("If you see the user above, try logging in with that EXACT Username.")

if __name__ == '__main__':
    list_employees()
