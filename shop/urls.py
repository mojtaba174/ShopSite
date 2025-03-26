from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('shop/<slug:slug>', views.detail_page, name='detail_page')
]
