from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,Group,Permission,User
# Create your models here.

class CustomeUser(AbstractUser):
    about_us = models.TextField(null=True,blank=True)
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
    

class Investment(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)  # Linking the transaction to a user
    products = models.ManyToManyField(Product, through='TransactionItem')  # Many-to-many relationship with products
    timestamp = models.DateTimeField(auto_now_add=True)


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Message(models.Model):
    sender = models.EmailField()
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    