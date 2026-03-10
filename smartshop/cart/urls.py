from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('', views.home, name='home'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_page, name='cart'),

path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart')

    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),

    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('login/', views.user_login, name='login'),

    path('register/', views.register, name='register'),

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('checkout/', views.checkout, name='checkout'),

    path('search/', views.search, name='search'),
]