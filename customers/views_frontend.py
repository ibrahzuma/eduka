from django.views.generic import ListView, CreateView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Customer
from .models import Customer
from .forms import CustomerForm
import csv
import io
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import redirect, render


class BaseShopView(LoginRequiredMixin):
    def get_shop(self):
        if hasattr(self.request.user, 'shops') and self.request.user.shops.exists():
            return self.request.user.shops.first()
        elif hasattr(self.request.user, 'employee_profile'):
             return self.request.user.employee_profile.shop
        return None

class ClientListView(BaseShopView, ListView):
    model = Customer
    template_name = 'customers/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return Customer.objects.filter(shop=shop).order_by('name')
        return Customer.objects.none()

class ClientCreateView(BaseShopView, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/client_form.html'
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        shop = self.get_shop()
        if not shop:
             messages.error(self.request, "No shop associated.")
             return self.form_invalid(form)
        form.instance.shop = shop
        messages.success(self.request, "Client added successfully!")
class ClientUpdateView(BaseShopView, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/client_form.html'
    success_url = reverse_lazy('client_list')

    def get_queryset(self):
        shop = self.get_shop()
        if shop:
            return Customer.objects.filter(shop=shop)
        return Customer.objects.none()

    def form_valid(self, form):
        messages.success(self.request, "Client updated successfully!")
        return super().form_valid(form)

class PlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/placeholder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.path.strip('/').replace('/', ' ').title()
        return context

class ClientImportView(BaseShopView, TemplateView):
    template_name = 'customers/client_import.html'

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            messages.error(request, "No file uploaded.")
            return redirect('client_import')

        if not file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect('client_import')

        shop = self.get_shop()
        if not shop:
             messages.error(request, "No shop found.")
             return redirect('dashboard')

        try:
            decoded_file = file.read().decode('utf-8-sig')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            field_names = reader.fieldnames
            if not field_names or 'Name (Jina)' not in field_names:
                 messages.error(request, "Invalid CSV format. Please use the provided template.")
                 return redirect('client_import')

            created_count = 0
            updated_count = 0
            errors = []

            with transaction.atomic():
                for index, row in enumerate(reader, start=1):
                    try:
                        name = row.get('Name (Jina)', '').strip()
                        if not name: continue
                        
                        phone = row.get('Phone (Simu)', '').strip()
                        email = row.get('Email', '').strip()
                        address = row.get('Address (Makazi)', '').strip()

                        customer, created = Customer.objects.get_or_create(
                            shop=shop, 
                            name=name,
                            defaults={'phone': phone, 'email': email, 'address': address}
                        )
                        
                        if not created:
                            # Update existing? Let's say yes for now, only if fields are empty or just update all?
                            # Standard behavior: Update if found (to allow corrections)
                            customer.phone = phone
                            customer.email = email
                            customer.address = address
                            customer.save()
                            updated_count += 1
                        else:
                            created_count += 1

                    except Exception as e:
                        errors.append(f"Row {index} ({name}): {str(e)}")

            if errors:
                messages.warning(request, f"Import finished. Created: {created_count}, Updated: {updated_count}. Some errors occurred.")
            else:
                messages.success(request, f"Successfully imported {created_count} new clients and updated {updated_count}.")

        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
        
        return redirect('client_list')

class ClientTemplateDownloadView(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="client_import_template.csv"'

        writer = csv.writer(response)
        headers = ['Name (Jina)', 'Phone (Simu)', 'Email', 'Address (Makazi)']
        writer.writerow(headers)
        
        # Example
        writer.writerow(['John Doe', '0712345678', 'john@example.com', 'Dar es Salaam'])
        
        return response
