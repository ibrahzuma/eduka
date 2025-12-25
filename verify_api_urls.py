import os
import django
from django.urls import resolve

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

def verify_api_urls():
    print("Verifying API URLs...")
    try:
        # Test URL resolution
        print(f"Resolving 'api/users/roles/': {resolve('/api/users/roles/')}")
        print(f"Resolving 'api/users/employees/': {resolve('/api/users/employees/')}")
        print("API URLs are correctly configured.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    verify_api_urls()
