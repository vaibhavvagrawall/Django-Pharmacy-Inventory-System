from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from .forms import UserRegisterForm, PharmacyItemForm, CategoryForm, UserUpdateForm
from pharmacy_app.models import PharmacyItem, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

def pharmacy_view(request):
    user = request.user
    template = loader.get_template('index.html')
    context = {
        'messages': messages.get_messages(request),
    }
    return HttpResponse(template.render(context, request))

def SignUpView(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!', extra_tags='action')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'updateprofile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been updated successfully.', extra_tags='action')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {'form': form})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.', extra_tags='action')
        return redirect('pharmacy_view')
    return render(request, 'deleteuser.html')

@login_required
def logout_user(request):
    """Handle the logout process and display a confirmation page."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out successfully.', extra_tags='action')
        return redirect('pharmacy_view') 
    
    return render(request, 'logout.html')

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        threshold = 10
        items = PharmacyItem.objects.filter(user=self.request.user).order_by('id')
        categories = Category.objects.filter(user=self.request.user)
        
        items_with_sno = enumerate(items, start=1)
        categories_with_sno = enumerate(categories, start=1)
        
        # Prepare alerts
        low_stock_alerts = [item for item in items if item.quantity <= threshold]
        alerts = [f"Alert: The quantity of '{item.name}' is low ({item.quantity})!" for item in low_stock_alerts]
        
        return render(request, 'dashboard.html', {
            'items_with_sno': items_with_sno,
            'categories_with_sno': categories_with_sno,
            'alerts': alerts
        })

class AddItem(LoginRequiredMixin, CreateView):
    model = PharmacyItem
    form_class = PharmacyItemForm
    template_name = 'itemform.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Item added successfully!', extra_tags='action')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)
        return context

class EditItem(LoginRequiredMixin, UpdateView):
    model = PharmacyItem
    form_class = PharmacyItemForm
    template_name = 'edititem.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Item updated successfully!', extra_tags='action')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)  # Filter categories by the current user
        return context

class DeleteItem(LoginRequiredMixin, DeleteView):
    model = PharmacyItem
    template_name = 'deleteitem.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, 'Item deleted successfully!', extra_tags='action')
        return response

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'passwordresetconfirm.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been successfully changed!', extra_tags='action')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error resetting your password. Please try again.')
        return super().form_invalid(form)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'passwordreset.html'
    email_template_name = 'passwordresetemail.html'
    subject_template_name = 'passwordresetsubject.txt'
    success_url = reverse_lazy('pharmacy_view')
    success_message = "A password reset email has been sent. Please check your email for further instructions."

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!', extra_tags='action')
            return redirect('dashboard') 
    else:
        form = CategoryForm()
    return render(request, 'addcategory.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        PharmacyItem.objects.filter(category=category).delete()
        category.delete()
        messages.success(request, 'Category and associated items deleted successfully!', extra_tags='action')
        return redirect('dashboard')
    return render(request, 'deletecategory.html', {'category': category})

class EditCategory(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'editcategory.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit Category'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Category updated successfully!', extra_tags='action')
        return response
