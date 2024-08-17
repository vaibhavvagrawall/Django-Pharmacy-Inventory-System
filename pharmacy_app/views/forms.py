from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from pharmacy_app.models import Category, PharmacyItem

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email','password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if'usable_password' in self.fields:
            del self.fields['usable_password']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class PharmacyItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),  # Initialize with no categories
        empty_label='-select category name-'
    )

    class Meta:
        model = PharmacyItem
        fields = ['name', 'company', 'quantity', 'category', 'price']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)
            
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
