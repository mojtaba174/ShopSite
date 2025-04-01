from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from cart.classes.cart import Cart
from shop.models import Product, ProductVariant
from .models import CartItem


def cart_page(request):
    if request.user.is_authenticated:
        cart = request.user.cart_item.all()
    else:
        cart = Cart(request)
    return render(request, 'cart/cart_page.html', context={'cart': cart})


def add_to_cart(request, slug):
    next = request.GET.get('next')
    variant_id = request.POST.get('variant_id')
    product = get_object_or_404(Product, slug=slug)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    if request.user.is_authenticated:
        if CartItem.objects.filter(user=request.user, product=product, variant=variant).exists():
            return redirect(f"{reverse('shop:cart:increase_cart_quantity', args=[slug, variant_id])}?next={next}")
        else:
            CartItem.objects.create(user=request.user, product=product, variant=variant, quantity=1,
                                    total_price=variant.price)
    else:
        cart = Cart(request)
        cart.add(product, variant_id)
    if next:
        return redirect(next)
    return redirect("shop:cart:cart_page")


def decrease_cart_quantity(request, slug, variant_id):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product, variant=variant)
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.total_price = cart_item.quantity * variant.price
            cart_item.save()
    else:
        cart = Cart(request)
        cart.add(product, variant_id, -1)
    if next:
        return redirect(next)
    return redirect("shop:cart:cart_page")


def increase_cart_quantity(request, slug, variant_id):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product, variant=variant)
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * variant.price
        cart_item.save()
    else:
        cart = Cart(request)
        cart.add(product, variant_id)
    if next:
        return redirect(next)
    return redirect("shop:cart:cart_page")
