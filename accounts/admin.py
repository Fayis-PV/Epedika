from django.contrib import admin
from .models import CustomeUser

# Register your models here.
class CustomeUserAdmin(admin.ModelAdmin):
    list_display = ['username','email']

admin.site.register(CustomeUser,CustomeUserAdmin)