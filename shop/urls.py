from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('shop/product/<slug:slug>', views.detail_page, name='detail_page'),
    path('shop/cart', views.cart_page, name='cart_page'),
    path('shop/add_to_cart/<slug:slug>', views.add_to_cart, name='add_to_cart'),
    path('shop/decrease_cart_quantity/<slug:slug>', views.decrease_cart_quantity, name='decrease_cart_quantity'),
    path('shop/remove_from_cart/<slug:slug>', views.remove_from_cart, name='remove_from_cart')
]
