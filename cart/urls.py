from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_page, name='cart_page'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('increase_cart_quantity/<int:variant_id>/', views.increase_cart_quantity,
         name='increase_cart_quantity'),
    path('decrease_cart_quantity/<int:variant_id>/', views.decrease_cart_quantity,
         name='decrease_cart_quantity'),
    path('confirm/', views.confirm, name='confirm')
]
