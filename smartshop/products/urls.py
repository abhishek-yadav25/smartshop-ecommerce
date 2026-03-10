from django.urls import path
from . import views

urlpatterns = [

    # Home / Products page
    path('', views.home, name='home'),

    # Product detail page
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),


    # Cart
    path('cart/', views.cart_page, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    # Cart controls
    path('increase/<int:id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),
]