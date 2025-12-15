from django.urls import path
from .views_frontend import ShopCreateView, BranchListView

urlpatterns = [
    path('create/', ShopCreateView.as_view(), name='shop_create'),
    path('branches/', BranchListView.as_view(), name='branch_list'),
]
