import barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
import os
from django.conf import settings

def generate_barcode(product_sku):
    """
    Generates a barcode image for a given SKU.
    Returns: BytesIO object containing the image.
    """
    # Use Code128 as it supports alphanumeric characters
    EAN = barcode.get_barcode_class('code128')
    
    # Create barcode object
    my_barcode = EAN(product_sku, writer=ImageWriter())
    
    # Save to a BytesIO buffer
    buffer = BytesIO()
    my_barcode.write(buffer)
    
    return buffer

def generate_pdf_labels(products):
    """
    Generates a PDF with barcode labels for a list of products.
    Each label contains: Product Name, Price, and Barcode.
    Layout: 3x7 grid on A4.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Label dimensions (approx 63.5mm x 38.1mm - standard Avery 3x7)
    label_width = 70 * mm
    label_height = 40 * mm
    margin_x = 0 * mm
    margin_y = 10 * mm
    
    x_start = margin_x
    y_start = height - margin_y - label_height
    
    x = x_start
    y = y_start
    
    col = 0
    row = 0
    
    for product in products:
        # Draw Label Border (Optional, helpful for cutting)
        p.setStrokeColorRGB(0.8, 0.8, 0.8)
        p.rect(x, y, label_width, label_height)
        
        # 1. Product Name (Truncated)
        p.setFont("Helvetica-Bold", 10)
        p.setFillColorRGB(0, 0, 0)
        name = product.name[:25] + "..." if len(product.name) > 25 else product.name
        p.drawCentredString(x + label_width/2, y + label_height - 10, name)
        
        # 2. Price
        p.setFont("Helvetica", 9)
        p.drawCentredString(x + label_width/2, y + label_height - 20, f"TZS {product.selling_price:,.0f}")
        
        # 3. Barcode Image
        # If product has no SKU, use ID prefixed
        sku = product.sku if product.sku else f"PRD{product.id:05d}"
        
        try:
            barcode_buffer = generate_barcode(sku)
            # Draw image from buffer
            # reportlab needs a file path or PIL image. 
            # We can use ImageReader from reportlab.lib.utils
            from reportlab.lib.utils import ImageReader
            barcode_buffer.seek(0)
            img = ImageReader(barcode_buffer)
            
            # Draw barcode at bottom
            p.drawImage(img, x + 5*mm, y + 2*mm, width=label_width - 10*mm, height=15*mm)
        except Exception as e:
            print(f"Error generating barcode details: {e}")
            p.drawString(x + 5*mm, y + 5*mm, f"SKU: {sku}")

        # Grid Logic
        col += 1
        x += label_width
        
        if col >= 3:
            col = 0
            x = x_start
            row += 1
            y -= label_height
            
        # New Page if full
        if row >= 7:
            p.showPage()
            x = x_start
            y = y_start
            col = 0
            row = 0
            
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer
