from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from cart.classes.cart import Cart
from shop.models import Product


def cart_page(request):
    cart = Cart(request)
    return render(request, 'cart/cart_page.html', context={'cart': cart})


def add_to_cart(request, slug):
    next = request.GET.get('next')
    variant_id = request.POST.get('variant_id')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)

    cart.add(product, variant_id)
    if next:
        return redirect(next)
    return redirect("shop:cart:cart_page")


def decrease_cart_quantity(request, slug, variant_id):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    cart.add(product, variant_id, -1)
    if next:
        return redirect(next)
    return redirect("shop:cart:cart_page")


def increase_cart_quantity(request, slug, variant_id):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    cart.add(product, variant_id)
    if next:
        return redirect(next)
    return redirect("shop:cart:cart_page")