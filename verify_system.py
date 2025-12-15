
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from rest_framework.test import APIClient
from users.models import CustomUser
from shops.models import Shop
import json

def run_verification():
    client = APIClient()
    print("Starting Verification Flow (APIClient)...")

    # 1. Register User
    print("\n[1] Registering User...")
    user_data = {
        'username': 'owner5',
        'password': 'password123',
        'email': 'owner5@example.com',
        'role': 'OWNER'
    }
    response = client.post('/api/auth/register/', user_data, format='json')
    if response.status_code == 201:
        print("User Registered Successfully.")
    else:
        print(f"Failed to register user: {response.status_code}")
        with open('register_error.html', 'wb') as f:
            f.write(response.content)
        print("Error content saved to register_error.html")
        return

    # 2. Login
    print("\n[2] Logging In...")
    login_data = {'username': 'owner5', 'password': 'password123'}
    response = client.post('/api/auth/login/', login_data, format='json')
    if response.status_code == 200:
        token = response.json()['access']
        print("Login Successful. Token received.")
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    else:
        print(f"Login failed: {response.content}")
        return

    # 3. Create Shop
    print("\n[3] Creating Shop...")
    shop_data = {'name': 'My Duka 2'}
    response = client.post('/api/shops/shops/', shop_data, format='json')
    if response.status_code == 201:
        shop_id = response.json()['id']
        branch_id = response.json()['branches'][0]['id'] # Main branch created auto
        print(f"Shop Created: {shop_id}, Main Branch: {branch_id}")
    else:
        print(f"Failed to create shop: {response.content}")
        return

    # 4. Create Category & Product
    print("\n[4] Creating Category & Product...")
    cat_data = {'name': 'Beverages', 'shop': shop_id}
    response = client.post('/api/inventory/categories/', cat_data, format='json')
    if response.status_code != 201:
        print(f"Failed to create category: {response.content}")
        return
    cat_id = response.json()['id']

    prod_data = {
        'name': 'Soda',
        'shop': shop_id,
        'category': cat_id,
        'selling_price': '1000.00',
        'product_type': 'GOODS'
    }
    response = client.post('/api/inventory/products/', prod_data, format='json')
    if response.status_code != 201:
        print(f"Failed to create product: {response.content}")
        return
    prod_id = response.json()['id']
    print(f"Product Created: {prod_id}")

    # 5. Add Stock
    stock_data = {'product': prod_id, 'branch': branch_id, 'quantity': 100}
    response = client.post('/api/inventory/stocks/', stock_data, format='json')
    if response.status_code == 201:
        print("Stock Added.")
    else:
        print(f"Failed to add stock: {response.content}")

    # 6. Make Sale
    print("\n[6] Making a Sale...")
    sale_data = {
        'shop': shop_id,
        'branch': branch_id,
        'items': [{'product': prod_id, 'quantity': 2, 'price': '1000.00'}]
    }
    response = client.post('/api/sales/sales/', sale_data, format='json')
    if response.status_code == 201:
        print("Sale Successful.")
        sale_id = response.json()['id']
    else:
        print(f"Sale failed: {response.content}")
        return

    # 7. Check Dashboard
    print("\n[7] Checking Dashboard...")
    response = client.get('/api/dashboard/summary/', format='json')
    if response.status_code == 200:
        data = response.json()
        print(f"Dashboard Data: {json.dumps(data, indent=2)}")
        if float(data.get('total_sales_volume', 0)) >= 2000.0:
            print("VERIFICATION SUCCESSFUL: Sales volume matches.")
        else:
            print(f"Verification Warning: Sales volume mismatch. Expected >= 2000, got {data.get('total_sales_volume')}")
    else:
        print(f"Dashboard failed: {response.content}")

if __name__ == '__main__':
    run_verification()
