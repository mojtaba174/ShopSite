from django.urls import path
from .views import add_comment

urlpatterns = [
    path('add/<slug:product_slug>/', add_comment, name='add_comment'),
]
