
import os
import django
from decimal import Decimal
from django.test import RequestFactory, Client
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from users.models import CustomUser
from shops.models import Shop, Branch, ShopSettings
from sales.models import Sale, SaleItem
from inventory.models import Product, Stock, Category
from sales.views_frontend import SaleDeleteView

def verify_sale_delete():
    print("Verifying Sales Deletion & Stock Restoration...")
    
    # 1. Setup Data
    sale_to_delete_id = None
    try:
        import time
        ts = int(time.time())
        
        # User & Shop
        user = CustomUser.objects.create_user(username=f"owner_{ts}", email=f"owner_{ts}@test.com", password="pass", role='OWNER')
        shop = Shop.objects.create(owner=user, name=f"Shop {ts}")
        ShopSettings.objects.create(shop=shop)
        branch = Branch.objects.create(shop=shop, name="Main", is_main=True)
        
        # Product
        cat = Category.objects.create(shop=shop, name="Gen")
        product = Product.objects.create(shop=shop, category=cat, name=f"Prod {ts}", selling_price=1000)
        
        # Initial Stock
        initial_qty = 100
        # Stock created by signal, so we get it and update
        stock = Stock.objects.get(branch=branch, product=product)
        stock.quantity = initial_qty
        stock.save()
        print(f"Initial Stock: {stock.quantity}")
        
        # create user connection mock 
        user.shops.add(shop) # Assuming related_name='shops' works or manually adding if needed for view logic
        
        # Create Sale
        sale_qty = 5
        sale = Sale.objects.create(shop=shop, branch=branch, cashier=user, total_amount=5000)
        sale_to_delete_id = sale.id
        SaleItem.objects.create(sale=sale, product=product, quantity=sale_qty, price=1000)
        
        # Deduct Stock (Simulate POS)
        stock.quantity -= sale_qty
        stock.save()
        print(f"Stock after Sale: {stock.quantity}")
        
        assert stock.quantity == 95
        
        # 2. Perform Delete
        # We use Client to simulate full request including middleware if needed, but View directly is easier for unit test style
        factory = RequestFactory()
        request = factory.post(f'/sales/delete/{sale.id}/') # POST confirms delete
        request.user = user
        
        # Add message support
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        view = SaleDeleteView.as_view()
        response = view(request, pk=sale.id)
        
        print(f"Delete Response Code: {response.status_code}")
        if response.status_code == 302:
            print(f"Redirected to: {response.url}")
            print("Redirected successfully (expected).")
        
        # 3. Verify
        # Check Sale Deleted
        if not Sale.objects.filter(id=sale.id).exists():
            print("PASS: Sale record deleted.")
        else:
            print("FAIL: Sale record still exists.")
            
        # Check Stock Restored
        stock.refresh_from_db()
        print(f"Stock after Delete: {stock.quantity}")
        
        if stock.quantity == initial_qty:
                print("PASS: Stock restored correctly.")
        else:
                print(f"FAIL: Stock not restored. Expected {initial_qty}, got {stock.quantity}")
                 
    except Exception as e:
        print(f"Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify_sale_delete()
