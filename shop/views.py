from django.shortcuts import render, get_object_or_404
from .models import Product


def home_page(request):
    products = Product.objects.all()
    return render(request, 'shop/home_page.html', {'products': products})


def detail_page(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/detail_page.html', {'product': product})
