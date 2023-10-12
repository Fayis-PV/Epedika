from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('',home,name='home'),
    path('json/',UserJsonView.as_view(),name='user-json'),
    # path('accounts/register/',RegisterView.as_view(),name='register'),

    path("categories", CategoryListView.as_view(), name="category_list"),
    path("categories/create", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>", CategoryDetailView.as_view(), name="category_detail"),

    path("products", ProductListView.as_view(), name="product_list"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product_detail"),

]
