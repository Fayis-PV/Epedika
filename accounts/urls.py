from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('',home,name='home'),
    path('json/',UserJsonView.as_view(),name='user-json'),
    path('accounts/register/',RegisterView.as_view(),name='register')



]
