from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('',home,name='home'),
    path('json/',UserJsonView.as_view(),name='user-json'),
    # path('accounts/register/',RegisterView.as_view(),name='register'),

    path("categories", CategoryListView.as_view(), name="category_list"),
    path("categories", CategoryCreateView.as_view(), name="category_list"),
    path("categories", CategoryListView.as_view(), name="category_list"),

    path("products", ProductListView.as_view(), name="product_list"),
    path("products", ProductCreateView.as_view(), name="product_list"),
    path("products", ProductListView.as_view(), name="product_list"),

]
