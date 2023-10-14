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
from .forms import CustomUserForm ,TransactionForm
from django.views.generic.edit import FormView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# @login_required
def home(request):
    return render(request,'index.html')


def custom_404(request, exception):
    return render(request, '404.html', status=status.HTTP_404_NOT_FOUND)

def custom_400(request, exception):
    return render(request, '400.html', status=400)


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
class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionCreateView(FormView):
    template_name = 'account/transaction.html'
    form_class = TransactionForm
    success_url = '/transactions/'  # Redirect to a transaction list page after successful submission

    def form_valid(self, form):
        # Handle successful form submission
        transaction = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle form validation errors
        # You can customize error handling here
        return super().form_invalid(form)


class MessageInboxView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(recipient=user).order_by('-timestamp')

class MessageSendingView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    authentication_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(sender=self.request.user)
        except Exception as e:
            return Response({'error': 'Message sending failed'}, status=status.HTTP_400_BAD_REQUEST)


class AddtoWishListView(generics.CreateAPIView):
    serializer_class = TransactionItemSerializer

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        user = request.user

        # Check if the product exists
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if there's an existing pending transaction for the user
        transaction, created = Transaction.objects.get_or_create(user=user, status=Transaction.PENDING)

        # Check if the item is already in the wishlist
        try:
            wishlist_item = TransactionItem.objects.get(transaction=transaction, product=product)
            wishlist_item.quantity = quantity
            wishlist_item.save()
        except ObjectDoesNotExist:
            wishlist_item = TransactionItem.objects.create(transaction=transaction, product=product, quantity=quantity)

        # Serialize the entire transaction with all its items
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(recipient=user).order_by('-timestamp')

class OrderProductsView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        user = request.user
        admin_user = User.objects.get(is_staff=True)

        # Check if there's an existing pending transaction for the user
        try:
            transaction = Transaction.objects.get(user=user, status='pending')
        except Transaction.DoesNotExist:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create a new order and update the transaction status
        order_transaction = Order.objects.create(sender=user, recipient=admin_user, transaction=transaction)
        order_transaction.save()
        transaction.status = 'ordered'
        transaction.save()
        serializer = OrderSerializer(order_transaction)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserOrderHistoryView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        user_transaction_history = Transaction.objects.filter(user=user, status='completed')
        
        if user_transaction_history:
            serializer = TransactionSerializer(user_transaction_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You have not any completed transactions with us.'}, status=status.HTTP_204_NO_CONTENT)

class OrderCompleteView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        user = request.user
        admin_user = User.objects.get(is_staff=True)

        try:
            transaction = Transaction.objects.get(user=user, status='ordered')
        except Transaction.DoesNotExist:
            return Response({'detail': 'No ordered transaction found for the user'}, status=status.HTTP_404_NOT_FOUND)

        try:
            order_transaction = Order.objects.get(transaction=transaction)
        except Order.DoesNotExist:
            return Response({'detail': 'No corresponding order found for the transaction'}, status=status.HTTP_404_NOT_FOUND)

        for product in transaction.products.all():
            try:
                transaction_item = TransactionItem.objects.get(transaction=transaction, product=product)
                quantity = transaction_item.quantity
                real_product = Product.objects.get(id=product.id)
                if real_product.stock < quantity:
                    return Response({'detail': 'Insufficient stock for a product in the order'}, status=status.HTTP_400_BAD_REQUEST)
                real_product.stock -= quantity
                real_product.save()
            except (TransactionItem.DoesNotExist, Product.DoesNotExist):
                return Response({'detail': 'Transaction item or product not found'}, status=status.HTTP_404_NOT_FOUND)

        transaction.status = 'completed'
        transaction.save()
        message = 'Thank you for purchasing the products successfully. Keep in touch.'
        user_message = Message.objects.create(sender=admin_user.email, recipient=user, message=message)
        user_message.save()

        order_transaction.answered = True
        order_transaction.save()

        serializer = OrderSerializer(order_transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderCancelView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        user = request.user
        admin_user = User.objects.get(is_staff=True)

        try:
            transaction = Transaction.objects.get(user=user, status='ordered')
        except Transaction.DoesNotExist:
            return Response({'detail': 'No ordered transaction found for the user'}, status=status.HTTP_404_NOT_FOUND)

        try:
            order_transaction = Order.objects.get(transaction=transaction)
        except Order.DoesNotExist:
            return Response({'detail': 'No corresponding order found for the transaction'}, status=status.HTTP_404_NOT_FOUND)

        transaction.status = 'canceled'
        transaction.save()

        message = 'Your order has been canceled. Keep in touch.'
        user_message = Message.objects.create(sender=admin_user.email, recipient=user, message=message)
        user_message.save()

        order_transaction.answered = True
        order_transaction.save()

        serializer = OrderSerializer(order_transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class SendSubscriptionMessageView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        # Get all subscribers who are subscribed
        subscribers = NewsletterSubscription.objects.filter(is_subscribed=True)

        if subscribers:
            subject = 'Subscription Update'
            message = 'Thank you for subscribing to our newsletters and promotions.'
            from_email = 'sender@example.com'

            # Send emails to subscribers
            for subscriber in subscribers:
                send_email(subject, message, from_email, [subscriber.user.email])

        return Response({"message": "Sending subscription emails to subscribers."})