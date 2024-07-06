from django.contrib import admin
from .models import PharmacyItem, Category
# Register your models here.

admin.site.register(PharmacyItem)
admin.site.register(Category)