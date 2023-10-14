from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,Group,Permission,User
from .fields import *
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
    market_price = models.PositiveIntegerField(default=0)
    our_price = models.PositiveIntegerField(default=0)
    image = models.URLField(null=True,blank=True)
    stock = models.IntegerField(default=0)
    rating = IntegerRangeField(null=True,blank=True,max_value=5,min_value=0)
    
    def __str__(self):
        return self.name
    

class Slides(models.Model):
    image = models.URLField()


# class Investment(models.Model):
#     user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    PENDING = 'pending'
    ORDERED = 'ordered'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ORDERED, 'Ordered'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking the transaction to a user
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    products = models.ManyToManyField(Product, through='TransactionItem')  # Many-to-many relationship with products
    timestamp = models.DateTimeField(auto_now_add=True)


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.EmailField()
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    

class Order(models.Model):
    sender = models.ForeignKey(User, related_name='sent_orders', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_orders', on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)