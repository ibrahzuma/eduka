from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Expense
from .forms import ExpenseForm

class BaseShopView(LoginRequiredMixin):
    def get_shop(self):
        if hasattr(self.request.user, 'shops') and self.request.user.shops.exists():
            return self.request.user.shops.first()
        elif hasattr(self.request.user, 'employee_profile'):
             return self.request.user.employee_profile.shop
        return None

class ExpenseListView(BaseShopView, ListView):
    model = Expense
    template_name = 'finance/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return Expense.objects.filter(shop=shop).order_by('-date')
        return Expense.objects.none()

class ExpenseCreateView(BaseShopView, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expense_form.html'
    success_url = reverse_lazy('expense_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['shop'] = self.get_shop()
        return kwargs

    def form_valid(self, form):
        shop = self.get_shop()
        if not shop:
             messages.error(self.request, "No shop associated.")
             return self.form_invalid(form)
        form.instance.shop = shop
        messages.success(self.request, "Expense recorded successfully!")
        return super().form_valid(form)

from .models import Income
from .forms import IncomeForm

class IncomeListView(BaseShopView, ListView):
    model = Income
    template_name = 'finance/income_list.html'
    context_object_name = 'incomes'

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return Income.objects.filter(shop=shop).order_by('-date')
        return Income.objects.none()

class IncomeCreateView(BaseShopView, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'finance/income_form.html'
    success_url = reverse_lazy('income_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['shop'] = self.get_shop()
        return kwargs

    def form_valid(self, form):
        shop = self.get_shop()
        if not shop:
             messages.error(self.request, "No shop associated.")
             return self.form_invalid(form)
        form.instance.shop = shop
        messages.success(self.request, "Income recorded successfully!")
        return super().form_valid(form)

class PlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/placeholder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.path.strip('/').replace('/', ' ').title()
        return context
