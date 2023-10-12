from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django import forms
from .models import CustomeUser

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomeUser
        fields = ['username','email','password']