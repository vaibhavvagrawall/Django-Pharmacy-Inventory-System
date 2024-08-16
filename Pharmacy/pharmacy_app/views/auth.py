from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate,login
from .forms import UserRegisterForm, PharmacyItemForm, CategoryForm
from pharmacy_app.models import PharmacyItem, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from Pharmacy.settings import LOW_QUANTITY
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

def pharmacy_view(request):
    user =request.user
    print(user)
    template=loader.get_template('index.html')
    return HttpResponse(template.render())

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = PharmacyItem.objects.filter(user=self.request.user.id).order_by('id')
        categories = Category.objects.all()

        # Generate sequential numbers for items and categories
        items_with_sno = enumerate(items, start=1)
        categories_with_sno = enumerate(categories, start=1)

        return render(request, 'dashboard.html', {'items_with_sno': items_with_sno, 'categories_with_sno': categories_with_sno})


class SignUpView(View):
    def get(self,request):
        form = UserRegisterForm()
        return render(request,'signup.html',{'form':form})
    def post(self,request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user=authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request,user)
            return redirect('pharmacy_view')
        return render(request,'signup.html',{'form':form})

class AddItem(LoginRequiredMixin,CreateView):
    model=PharmacyItem
    form_class=PharmacyItemForm
    template_name='itemform.html'
    success_url=reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
       context=super().get_context_data(**kwargs)
       context['categories']=Category.objects.all()
       return context 

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class EditItem(LoginRequiredMixin,UpdateView):
    model=PharmacyItem
    form_class=PharmacyItemForm
    template_name='edititem.html'
    success_url=reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin,DeleteView):
    model=PharmacyItem
    template_name='deleteitem.html'
    success_url=reverse_lazy('dashboard')
    context_object_name='item'

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'passwordreset.html'
    email_template_name = 'passwordresetemail.html'
    subject_template_name = 'passwordresetsubject.txt'
    success_url = reverse_lazy('pharmacy_view')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = CategoryForm()
    return render(request, 'addcategory.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        # Delete all items related to this category
        PharmacyItem.objects.filter(category=category).delete()
        # Delete the category itself
        category.delete()
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

