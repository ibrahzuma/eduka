import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from users.models import CustomUser, Role

def diagnose_sidebar():
    print(">>> DIAGNOSING SIDEBAR VISIBILITY")
    
    employees = CustomUser.objects.filter(role='EMPLOYEE')
    print(f"Total Employees: {employees.count()}")
    
    if employees.count() == 0:
        print("No employees found to diagnose.")
        return

    for emp in employees:
        print(f"\nEmployee: {emp.username}")
        if not emp.assigned_role:
            print("  [!] NO ASSIGNED ROLE (Sidebar will be empty/default)")
            continue
            
        role = emp.assigned_role
        print(f"  Role: {role.name} (ID: {role.id})")
        print(f"  Permissions (Raw JSON): {role.permissions}")
        
        # Simulate check
        perms = role.permissions
        if not perms:
            print("  [CRITICAL] Permissions are EMPTY! Sidebar will be blank.")
        else:
            dashboard_access = 'view' in perms.get('dashboard', [])
            sales_access = 'view' in perms.get('sales', [])
            print(f"  - Can View Dashboard? {dashboard_access}")
            print(f"  - Can View Sales? {sales_access}")
            
            if not dashboard_access:
                print("  [WARNING] 'Dashboard' permission is missing. User has no landing page link!")

if __name__ == '__main__':
    diagnose_sidebar()
