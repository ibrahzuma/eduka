
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduka_backend.settings')
django.setup()

from users.models import CustomUser

try:
    print("Attempting to create user manually via create_user...")
    user = CustomUser.objects.create_user(
        username='testreg',
        password='password',
        email='test@e.com',
        phone='1234567890',
        role='OWNER'
    )
    print(f"Manual create_user success: {user.username}")
    user.delete()
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Manual create_user failed: {e}")
