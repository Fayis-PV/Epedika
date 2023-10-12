from django.shortcuts import render
from django.views import View
from .forms import CustomUserForm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import *

# Create your views here.
# @login_required
def home(request):
    return render(request,'index.html')


class UserJsonView(APIView):
    permission_classes =  [IsAuthenticated]

    def get(self,request):
        return Response({
            'email' : request.user.email
        })

class RegisterView(View):
    form = CustomUserForm
    template_name = '/registration/register.html'


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()