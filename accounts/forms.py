from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django import forms
from .models import CustomeUser,Transaction

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomeUser
        fields = ['username','email','password']


class TransactionForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, max_value=100)
    class Meta:
        model = Transaction
        fields = ['user', 'products','quantity']


