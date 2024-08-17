from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate,login, update_session_auth_hash, get_user_model, logout
from .forms import UserRegisterForm, PharmacyItemForm, CategoryForm, UserUpdateForm
from pharmacy_app.models import PharmacyItem, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from Pharmacy.settings import LOW_QUANTITY
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

def pharmacy_view(request):
    user = request.user
    print(user)
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
            messages.success(request, 'Your profile has been updated successfully!')
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
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {'form': form})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('pharmacy_view')  # Redirect to a different view or page after deletion
    return render(request, 'deleteuser.html')

@login_required
def logout_user(request):
    """Handle the logout process and display a confirmation page."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('pharmacy_view')  # Redirect to the homepage or another page
    
    # If accessed via GET, show confirmation page
    return render(request, 'logout.html')

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = PharmacyItem.objects.filter(user=self.request.user.id).order_by('id')
        categories = Category.objects.all()
        

        items_with_sno = enumerate(items, start=1)
        categories_with_sno = enumerate(categories, start=1)

        return render(request, 'dashboard.html', {'items_with_sno': items_with_sno, 'categories_with_sno': categories_with_sno})

class AddItem(LoginRequiredMixin, CreateView):
    model = PharmacyItem
    form_class = PharmacyItemForm
    template_name = 'itemform.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user for the PharmacyItem
        response = super().form_valid(form)
        messages.success(self.request, 'Item added successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)  # Filter categories by the current user
        return context

class EditItem(LoginRequiredMixin,UpdateView):
    model=PharmacyItem
    form_class=PharmacyItemForm
    template_name='edititem.html'
    success_url=reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Item updated successfully!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)  # Filter categories by the current user
        return context

class DeleteItem(LoginRequiredMixin,DeleteView):
    model=PharmacyItem
    template_name='deleteitem.html'
    success_url=reverse_lazy('dashboard')
    context_object_name='item'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, 'Item deleted successfully!')
        return response

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'passwordreset.html'
    email_template_name = 'passwordresetemail.html'
    subject_template_name = 'passwordresetsubject.txt'
    success_url = reverse_lazy('pharmacy_view')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('dashboard') 
    else:
        form = CategoryForm()
    return render(request, 'addcategory.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        PharmacyItem.objects.filter(category=category).delete()
        category.delete()
        messages.success(request, 'Category and associated items deleted successfully!')
        return redirect('dashboard')
    return render(request, 'deletecategory.html', {'category': category})

class EditCategory(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'editcategory.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit Category'
        return context

        def form_valid(self, form):
            response = super().form_valid(form)
            messages.success(self.request, 'Category updated successfully!')
            return response