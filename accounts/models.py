from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,Group,Permission
# Create your models here.

class CustomeUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_set'
    )

class Category(models.Model):
    name = models.CharField( max_length=50)
    description = models.TextField(null=True,blank=True)
    image = models.URLField(null=True,blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField( max_length=50)
    description = models.TextField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    price = models.PositiveIntegerField(default=0)
    image = models.URLField(null=True,blank=True)
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    

class Slides(models.Model):
    image = models.URLField()
    