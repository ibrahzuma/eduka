import os
import sys
import traceback

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')

print("--- Attempting to load Django... ---")
try:
    import django
    django.setup()
    print("Django Setup: SUCCESS")
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("WSGI Application Load: SUCCESS")
    print("--- The code is likely fine. Issue is with Gunicorn/Nginx. ---")
    
except Exception:
    print("--- FAILURE! Code crashed on startup. ---")
    traceback.print_exc()
