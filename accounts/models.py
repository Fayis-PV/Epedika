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
    description = models.TextField()
    created_on = models.DateField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField( max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length=500)
    stock = models.IntegerField(default=0)

class Slides(models.Model):
    image = models.URLField(max_length=500)
    