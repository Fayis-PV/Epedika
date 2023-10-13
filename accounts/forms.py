from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django import forms
from .models import CustomeUser,Transaction

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomeUser
        fields = ['username','email','password']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user', 'products']


