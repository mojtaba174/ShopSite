from django.urls import path
from . import views


app_name = 'comment'
urlpatterns = [
    path('add/<slug:product_slug>/', views.add_comment, name='add_comment'),
]
