from rest_framework import routers
from .views import ExpenseViewSet

router = routers.DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = router.urls
