
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from users.models import CustomUser

try:
    user = CustomUser.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    print("Successfully reset password for user 'admin' to 'admin123'.")
except CustomUser.DoesNotExist:
    print("User 'admin' does not exist. Creating new superuser...")
    CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created new superuser 'admin' with password 'admin123'.")
except Exception as e:
    print(f"Error: {e}")
