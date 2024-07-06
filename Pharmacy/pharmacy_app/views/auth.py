from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate,login
from .forms import UserRegisterForm, PharmacyItemForm
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

class Dashboard(LoginRequiredMixin,View):
    def get(self,request):
        items = PharmacyItem.objects.filter(user=self.request.user.id).order_by('id')
        low_inventory = PharmacyItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		)
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item has low inventory')
		
        low_inventory_ids = PharmacyItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

        return render(request,'dashboard.html',{'items':items})

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