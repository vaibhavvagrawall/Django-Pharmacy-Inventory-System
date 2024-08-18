from django.db import models
from django.contrib.auth.models import User

class PharmacyItem(models.Model):
    name=models.CharField(max_length=100)
    company=models.CharField(max_length=200)
    quantity=models.PositiveIntegerField()
    category=models.ForeignKey('Category',on_delete=models.CASCADE,blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name