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

    path("slides", SlideListCreateView.as_view(), name="slides_list"),
    path("slides/<int:pk>", SlideDetailView.as_view(), name="slides_detail"),

    path("transactions", TransactionListView.as_view(), name="transaction_list"),
    path("transactions/create", TransactionCreateView.as_view(), name="transaction_create"),

    path('inbox', MessageInboxView.as_view(), name='inbox'),
    path('send', MessageSendingView.as_view(), name='send_message'),

    path('add_to_wishlist', AddtoWishListView.as_view(), name='add_to_wishlist'),
    path('order_products', OrderProductsView.as_view(), name='order_products'),
    path('order_history', UserOrderHistoryView.as_view(), name='order_history'),
    path('orders', OrdersListView.as_view(), name='admin_orders'),
    path('complete_order', OrderCompleteView.as_view(), name='complete_order'),
    path('cancel_order', OrderCancelView.as_view(), name='cancel_order'),

    path('send-subscription-emails', SendSubscriptionMessageView.as_view(), name='send-subscription-emails'),
    path('subscriber',SubscribersView.as_view(),name='subcriber_view'),

    
    

    
    


]
