import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from shops.models import Shop, Branch
from sales.models import Sale
from dashboard.views import DashboardTemplateView
from django.test import RequestFactory
from django.utils import timezone

User = get_user_model()

def test_employee_management():
    print(">>> Setting up test data...")
    # Setup Owner and Shop
    owner_email = "owner_test_emp@example.com"
    if User.objects.filter(email=owner_email).exists():
        User.objects.filter(email=owner_email).delete()
        
    owner = User.objects.create_user(username="owner_test_emp", email=owner_email, password="password123", role='OWNER')
    shop = Shop.objects.create(owner=owner, name="Test Shop Emp")
    branch = Branch.objects.create(shop=shop, name="Main Branch")
    
    print(f"Created Owner: {owner} and Shop: {shop}")

    # 1. Create Employee (Simulating View Logic)
    print("\n>>> Testing Employee Creation...")
    employee = User.objects.create_user(username="emp_test", email="emp@test.com", password="password123", role='EMPLOYEE')
    # Assign Shop and Branch
    employee.shop = shop
    employee.branch = branch
    employee.save()
    
    print(f"Created Employee: {employee.username}, Shop: {employee.shop.name}, Branch: {employee.branch.name}")
    assert employee.shop == shop
    assert employee.branch == branch
    
    # 2. Update Employee (Password & Branch)
    print("\n>>> Testing Employee Update...")
    new_branch = Branch.objects.create(shop=shop, name="Second Branch")
    employee.branch = new_branch
    employee.set_password("newpassword456")
    employee.save()
    
    employee.refresh_from_db()
    assert employee.branch == new_branch
    assert employee.check_password("newpassword456")
    print("Employee updated successfully (Branch & Password)")

    # 3. Suspend
    print("\n>>> Testing Suspension...")
    employee.is_active = False
    employee.save()
    assert not employee.is_active
    print("Employee suspended.")
    
    employee.is_active = True
    employee.save()
    print("Employee reactivated.")

    # 4. Check Dashboard Logic
    print("\n>>> Testing Dashboard Filtering...")
    # Create Sales
    Sale.objects.create(shop=shop, branch=branch, cashier=owner, total_amount=1000)
    Sale.objects.create(shop=shop, branch=branch, cashier=employee, total_amount=500)
    
    # Test Owner View
    view = DashboardTemplateView()
    factory = RequestFactory()
    request = factory.get('/')
    request.user = owner
    view.request = request
    context = view.calculate_stats({}, 'today')
    print(f"Owner Total Sales: {context['total_sales_volume']} (Expected 1500)")
    assert context['total_sales_volume'] == 1500

    # Test Employee View
    request.user = employee
    view.request = request
    context = view.calculate_stats({}, 'today')
    print(f"Employee Total Sales: {context['total_sales_volume']} (Expected 500)")
    assert context['total_sales_volume'] == 500
    print(f"Employee Purchases: {context['total_purchases_volume']} (Expected 0)")
    assert context['total_purchases_volume'] == 0

    # 5. Delete
    print("\n>>> Testing Deletion...")
    user_id = employee.id
    employee.delete()
    assert not User.objects.filter(id=user_id).exists()
    print("Employee deleted successfully.")
    
    # Cleanup
    owner.delete() # CASCADEs shop
    print("\nAll Tests Passed!")

if __name__ == '__main__':
    try:
        test_employee_management()
    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()
