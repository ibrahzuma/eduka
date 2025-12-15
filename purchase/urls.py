from rest_framework import routers
from .views import SupplierViewSet, PurchaseOrderViewSet

router = routers.DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'orders', PurchaseOrderViewSet, basename='purchase-order')

urlpatterns = router.urls
