from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .forms import UserRegistrationForm

class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'OWNER' # Enforce Owner role
            user.save()
            
            # Extract Business Data from Form
            business_name = form.cleaned_data.get('business_name')
            # business_type = form.cleaned_data.get('business_type') # Not in Shop model yet, ignore or add to description
            region = form.cleaned_data.get('region')
            district = form.cleaned_data.get('district')
            street = form.cleaned_data.get('street')
            
            # Create Shop automatically
            from shops.models import Shop, Branch, ShopSettings
            shop = Shop.objects.create(owner=user, name=business_name)
            ShopSettings.objects.create(shop=shop)
            
            # Create Main Branch with Location Info
            address_str = f"{region}, {district}, {street}"
            Branch.objects.create(shop=shop, name='Main Branch', address=address_str, is_main=True)

            # Specify the backend to avoid MultipleBackends error
            # Using ModelBackend as default for registration-based login usually matches ModelBackend behavior
            # even if PhoneBackend is present. 
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('dashboard')
        return render(request, 'auth/register.html', {'form': form})

def custom_logout_view(request):
    if request.method == 'POST':
        from django.contrib.auth import logout
        logout(request)
        return redirect('login')
    return render(request, 'auth/logout.html')

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Role
from .forms import RoleForm
from django.contrib import messages

class RoleListView(LoginRequiredMixin, View):
    def get(self, request):
        roles = Role.objects.all().order_by('-created_at')
        form = RoleForm()
        return render(request, 'users/role_list.html', {'roles': roles, 'form': form})

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role created successfully!', extra_tags='success')
            return redirect('role_list')
        
        roles = Role.objects.all().order_by('-created_at')
        return render(request, 'users/role_list.html', {'roles': roles, 'form': form})

class RoleCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = RoleForm()
        # Define available permissions modules
        modules = [
            'Dashboard', 'Sales', 'Purchases', 'Products', 'Services', 'Inventory', 
            'Returns', 'Clients', 'Finance', 'Expenses', 'Reports', 'Branches', 'Users', 'Settings'
        ]
        return render(request, 'users/role_create.html', {'form': form, 'modules': modules})

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            
            # Process Permissions
            permissions = {}
            modules = [
                'Dashboard', 'Sales', 'Purchases', 'Products', 'Services', 'Inventory', 
                'Returns', 'Clients', 'Finance', 'Expenses', 'Reports', 'Branches', 'Users', 'Settings'
            ]
            for module in modules:
                module_lower = module.lower()
                module_perms = []
                if request.POST.get(f'{module_lower}_view'): module_perms.append('view')
                if request.POST.get(f'{module_lower}_create'): module_perms.append('create')
                if request.POST.get(f'{module_lower}_edit'): module_perms.append('edit')
                if request.POST.get(f'{module_lower}_delete'): module_perms.append('delete')
                
                if module_perms:
                    permissions[module_lower] = module_perms
            
            role.permissions = permissions
            role.save()
            messages.success(request, 'Role created successfully with permissions!', extra_tags='success')
            return redirect('role_list')
        
        modules = [
            'Dashboard', 'Sales', 'Purchases', 'Products', 'Services', 'Inventory', 
            'Returns', 'Clients', 'Finance', 'Expenses', 'Reports', 'Branches', 'Users', 'Settings'
        ]
        return render(request, 'users/role_create.html', {'form': form, 'modules': modules})

from .forms import EmployeeForm
from django.contrib.auth import get_user_model
User = get_user_model()

class EmployeeListView(LoginRequiredMixin, View):
    def get(self, request):
        # Filter users who are marked as employees
        employees = User.objects.filter(role='EMPLOYEE').order_by('-date_joined')
        return render(request, 'users/employee_list.html', {'employees': employees})

class EmployeeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'users/employee_create.html', {'form': form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!', extra_tags='success')
            return redirect('employee_list')
        return render(request, 'users/employee_create.html', {'form': form})

from .forms import ProfileForm

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'users/profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!', extra_tags='success')
            return redirect('profile')
        return render(request, 'users/profile.html', {'form': form})
