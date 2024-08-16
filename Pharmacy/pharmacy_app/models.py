from django.db import models
from django.contrib.auth.models import User

class PharmacyItem(models.Model):
    name=models.CharField(max_length=200)
    company=models.CharField(max_length=200)
    quantity=models.IntegerField()
    category=models.ForeignKey('Category',on_delete=models.CASCADE,blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Category(models.Model): 
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name