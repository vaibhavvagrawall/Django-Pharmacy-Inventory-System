from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from pharmacy_app.models import Category, PharmacyItem

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    
class PharmacyItemForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=Category.objects,initial=0)
    class Meta:
        model=PharmacyItem
        fields=['name','company','quantity','category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']