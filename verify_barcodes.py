
import os
import django
import io
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from inventory.utils import generate_barcode, generate_pdf_labels
from inventory.models import Product
from users.models import CustomUser
from shops.models import Shop

def verify_barcodes():
    print("Verifying Barcode Generation...")
    
    # 1. Test Single Barcode Generation
    sku = "TEST-SKU-123"
    print(f"Generating Barcode for SKU: {sku}")
    try:
        buffer = generate_barcode(sku)
        size = buffer.getbuffer().nbytes
        print(f"SUCCESS: Barcode image generated. Size: {size} bytes")
    except Exception as e:
        print(f"FAILURE: Barcode generation failed: {e}")
        return

    # 2. Test PDF Generation
    print("\nVerifying PDF Label Generation...")
    
    # Ensure we have a product
    user = CustomUser.objects.first()
    if not user:
        print("No user found, creating dummy.")
        user = CustomUser.objects.create(username="barcode_test", email="b@t.com")
        
    shop, _ = Shop.objects.get_or_create(name="Barcode Shop", owner=user)
    product, _ = Product.objects.get_or_create(shop=shop, name="Barcode Product", defaults={'selling_price': 500})
    
    try:
        pdf_buffer = generate_pdf_labels([product])
        pdf_size = pdf_buffer.getbuffer().nbytes
        print(f"SUCCESS: PDF Labels generated. Size: {pdf_size} bytes")
        
        # Optional: Save to verify manually
        with open("verify_barcode_output.pdf", "wb") as f:
            f.write(pdf_buffer.getvalue())
        print("Saved 'verify_barcode_output.pdf' for manual inspection.")
        
    except Exception as e:
        print(f"FAILURE: PDF generation failed: {e}")

if __name__ == '__main__':
    verify_barcodes()
