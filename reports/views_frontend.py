from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncDate
from sales.models import Sale
from purchase.models import PurchaseOrder
from finance.models import Expense
from inventory.models import Product, Stock
import datetime

class BaseShopView(LoginRequiredMixin):
    def get_shop(self):
        if hasattr(self.request.user, 'shops') and self.request.user.shops.exists():
            return self.request.user.shops.first()
        elif hasattr(self.request.user, 'employee_profile'):
             return self.request.user.employee_profile.shop
        return None

class SalesReportView(BaseShopView, ListView):
    model = Sale
    template_name = 'reports/sales_report.html'
    context_object_name = 'sales'

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return Sale.objects.filter(shop=shop).order_by('-created_at')
        return Sale.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = self.get_shop()
        if shop:
            context['total_sales'] = Sale.objects.filter(shop=shop).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            context['total_count'] = Sale.objects.filter(shop=shop).count()
        return context

class PurchasesReportView(BaseShopView, ListView):
    model = PurchaseOrder
    template_name = 'reports/purchases_report.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return PurchaseOrder.objects.filter(shop=shop).order_by('-created_at')
        return PurchaseOrder.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = self.get_shop()
        if shop:
            context['total_purchases'] = PurchaseOrder.objects.filter(shop=shop).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return context

class ExpensesReportView(BaseShopView, ListView):
    model = Expense
    template_name = 'reports/expenses_report.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return Expense.objects.filter(shop=shop).order_by('-date')
        return Expense.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = self.get_shop()
        if shop:
            context['total_expenses'] = Expense.objects.filter(shop=shop).aggregate(Sum('amount'))['amount__sum'] or 0
        return context

class IncomeStatementView(BaseShopView, TemplateView):
    template_name = 'reports/income_statement.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = self.get_shop()
        if shop:
            total_sales = Sale.objects.filter(shop=shop).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            total_purchases = PurchaseOrder.objects.filter(shop=shop).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
            total_expenses = Expense.objects.filter(shop=shop).aggregate(Sum('amount'))['amount__sum'] or 0
            
            context['total_income'] = total_sales
            context['total_cogs'] = total_purchases # Approximation for now
            context['gross_profit'] = total_sales - total_purchases
            context['total_expenses'] = total_expenses
            context['net_profit'] = context['gross_profit'] - total_expenses
        return context

class PlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/placeholder.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.path.strip('/').replace('/', ' ').replace('-', ' ').title()
        return context

class PricingReportView(BaseShopView, ListView):
    model = Product
    template_name = 'reports/pricing_report.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            # Calculate margin? Simple list for now showing Cost vs Price
            return Product.objects.filter(shop=shop)
        return Product.objects.none()

class DisposalReportView(BaseShopView, ListView):
    """Showing items with 0 stock or explicitly marked as disposed (future feature)"""
    model = Stock
    template_name = 'reports/disposal_report.html'
    context_object_name = 'disposals'
    
    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return Stock.objects.filter(branch__shop=shop, quantity=0)
        return Stock.objects.none()

class CashflowView(BaseShopView, TemplateView):
    template_name = 'reports/cashflow.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = self.get_shop()
        if shop:
            # Simple Cashflow: Inflow (Sales) vs Outflow (Purchases + Expenses)
            total_sales = Sale.objects.filter(shop=shop).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            total_purchases = PurchaseOrder.objects.filter(shop=shop).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
            total_expenses = Expense.objects.filter(shop=shop).aggregate(Sum('amount'))['amount__sum'] or 0
            
            context['inflow'] = total_sales
            context['outflow'] = total_purchases + total_expenses
            context['net_cashflow'] = context['inflow'] - context['outflow']
        return context
