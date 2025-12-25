
import os
import django
from django.utils import timezone
import datetime
from django.test import RequestFactory
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from users.models import CustomUser
from shops.models import Shop, Branch, ShopSettings
from sales.models import Sale
from reports.api_views import SalesSummaryAPIView

def verify_sales_api():
    print("Verifying Sales Summary API...")
    
    # 1. Setup Data
    timestamp = int(timezone.now().timestamp())
    username = f"sales_test_{timestamp}"
    user = CustomUser.objects.create_user(username=username, password='password123')
    shop = Shop.objects.create(owner=user, name=f"Sales Shop {timestamp}")
    Branch.objects.create(shop=shop, name="Main", is_main=True)
    ShopSettings.objects.create(shop=shop)
    
    print(f"Created User: {username}, Shop: {shop.name}")

    # Helper to create sale
    def create_sale(date_offset, amount):
        sale = Sale.objects.create(
            shop=shop,
            branch=Branch.objects.get(shop=shop),
            cashier=user,
            total_amount=Decimal(amount)
        )
        sale.created_at = timezone.now() - datetime.timedelta(days=date_offset)
        sale.save()
        return sale

    # 2. Create Sales
    # Today: 2 sales, total 3000
    create_sale(0, 1000)
    create_sale(0, 2000)
    
    # Week (3 days ago): 1 sale, total 5000
    create_sale(3, 5000)
    
    # Month (15 days ago): 1 sale, total 10000
    create_sale(15, 10000)
    
    # Year (200 days ago): 1 sale, total 50000
    create_sale(200, 50000)
    
    # Older (> 1 year): 1 sale, total 100000 (Should not appear in any)
    create_sale(400, 100000)
    
    # Expected Results
    # Today: 3000 (2)
    # Week (last 7 days): 3000 + 5000 = 8000 (3)
    # Month (last 30 days): 8000 + 10000 = 18000 (4)
    # Year (last 365 days): 18000 + 50000 = 68000 (5)
    
    # 3. Call API
    factory = RequestFactory()
    request = factory.get('/api/reports/sales/summary/')
    request.user = user
    
    view = SalesSummaryAPIView.as_view()
    response = view(request)
    
    if response.status_code != 200:
        print(f"FAILURE: Status Code {response.status_code}")
        print(response.data)
        return

    data = response.data
    print("API Response:", data)
    
    # 4. Verify
    try:
        # Today
        assert data['today']['total_sales'] == 3000
        assert data['today']['count'] == 2
        print("PASS: Today stats correct.")
        
        # Week
        assert data['week']['total_sales'] == 8000
        assert data['week']['count'] == 3
        print("PASS: Week stats correct.")
        
        # Month
        assert data['month']['total_sales'] == 18000
        assert data['month']['count'] == 4
        print("PASS: Month stats correct.")
        
        # Year
        assert data['year']['total_sales'] == 68000
        assert data['year']['count'] == 5
        print("PASS: Year stats correct.")
        
        print("SUCCESS: All checks passed.")
        
    except AssertionError as e:
        print(f"FAILURE: Assertion failed - {e}")

if __name__ == '__main__':
    verify_sales_api()
