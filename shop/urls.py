from django.urls import path, include
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('shop/product/<slug:slug>/', views.detail_page, name='detail_page'),
    path('shop/cart/', include('cart.urls')),
    path('shop/filter_category/<slug:slug>/', views.filter_category, name='filter_category'),
    path('shop/search_results/', views.search_results, name='search_results'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
]
