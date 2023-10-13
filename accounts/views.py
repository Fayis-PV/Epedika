from django.shortcuts import render
from django.views import View
# from .forms import CustomUserForm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import *
from .serializers import *
from django.shortcuts import render,redirect
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
from allauth.account.views import LogoutView,LoginView,SignupView,ConfirmEmailView
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.conf import settings
from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.urls import reverse
from rest_framework import viewsets

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

#User Authentication

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AdminPageView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        token = self.request.COOKIES.get('refresh_token')
        try:
            # Decode the JWT token's payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Extract the user's unique identifier
            user_id = payload.get('user_id')
            
            # Query the user database to retrieve the user
            user = User.objects.get(id=user_id)
            
            products = Product.objects.all().order_by('-added_on')
            categories = Category.objects.all().order_by('name')
            return Response({'User':user.username,
                             'Products':{products.first().name},
                             'Categories':{categories.first().name} })
        
        except jwt.ExpiredSignatureError:
            # Handle token expiration
            return None
        except jwt.DecodeError:
            # Handle invalid token
            return None
        except User.DoesNotExist:
            # Handle user not found
            return None
        

class CustomSignupView(SignupView):
    def get(self,request):
        return render(request,'account/signup.html')
    
    def form_valid(self, form):
        # Create the user but don't log them in
        self.user = form.save(self.request)
        return redirect("account_login")  # Redirect to the login page

    # Optional: Override the success url to redirect after email confirmation
    def get_success_url(self):
        return reverse("account_login")  # Redirect to the login page


class CustomLoginView(LoginView):
    def get(self,request):
        return render(request,'account/login.html')
    
    def form_valid(self, form):
        # Call the parent class's form_valid to complete the login process
        response = super().form_valid(form)
        
        # Generate and set JWT token as a cookie
        user = form.user
        refresh = MyTokenObtainPairSerializer.get_token(user)
        access_token = refresh.access_token
        
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True)

        return response


class CustomLogoutView(LogoutView):
    def get(self,request):
        return render(request,'account/logout.html')
    
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)

        # Delete the 'refresh_token' and 'user_session_id' cookies
        response.delete_cookie('refresh_token')
        response.delete_cookie('user_session_id')

        return response
         

# Product Management

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#Admin Panel Works 
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
