from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('',home,name='home'),
    path('signup', CustomSignupView.as_view(), name='signup'),
    path('login',CustomLoginView.as_view(),name= 'login'),
    path('logout',CustomLogoutView.as_view(),name= 'logout'),
    path("admin", AdminPageView.as_view(), name="admin_page"),

    path("categories", CategoryListView.as_view(), name="category_list"),
    path("categories/create", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>", CategoryDetailView.as_view(), name="category_detail"),

    path("products", ProductListView.as_view(), name="product_list"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product_detail"),

    path("slides", ProductListView.as_view(), name="slides_list"),
    path("slides/create", ProductCreateView.as_view(), name="slides_create"),
    path("slides/<int:pk>", ProductDetailView.as_view(), name="slides_detail"),

    path("transactions", TransactionListView.as_view(), name="transaction_list"),
    path("transactions/create", TransactionCreateView.as_view(), name="transaction_create"),

    path('inbox/', MessageInboxView.as_view(), name='inbox'),
    path('send/', MessageSendingView.as_view(), name='send_message'),


]
