from rest_framework import routers
from .views import SaleViewSet

router = routers.DefaultRouter()
router.register(r'sales', SaleViewSet, basename='sale')

urlpatterns = router.urls
