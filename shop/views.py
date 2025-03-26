from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .classes.cart import Cart


def home_page(request):
    products = Product.objects.all()
    return render(request, 'shop/home_page.html', {'products': products})


def detail_page(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/detail_page.html', {'product': product})


def cart_page(request):
    cart = Cart(request)
    return render(request, 'shop/cart_page.html', context={'cart': cart})


def add_to_cart(request, slug):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)

    cart.add(product)
    if next:
        return redirect(next)
    return redirect("shop:cart_page")

def decrease_cart_quantity(request, slug):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    cart.add(product, -1)
    if next:
        return redirect(next)
    return redirect("shop:cart_page")

def remove_from_cart(request, slug):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    cart.remove(product)
    if next:
        return redirect(next)
    return redirect("shop:cart_page")


