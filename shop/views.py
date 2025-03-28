from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, DigitCategory
from .classes.cart import Cart
from django.contrib import messages
from shop.models import Product
from .forms import CommentForm
from django.http import JsonResponse


def home_page(request):
    products = Product.objects.all()
    digit_categories = DigitCategory.objects.all()
    return render(request, 'shop/home_page.html', {'products': products, 'digit_categories': digit_categories})


def detail_page(request, slug):
    product = get_object_or_404(Product, slug=slug)

    comments = product.comments.select_related('user').order_by('-created_at')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, "کامنت شما با موفقیت ثبت شد! 🎉")
            return redirect('shop:detail_page', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'shop/detail_page.html', {
        'product': product,
        'comments': comments,
        'form': form
    })


def cart_page(request):
    cart = Cart(request)
    return render(request, 'shop/cart_page.html', context={'cart': cart})


def add_to_cart(request, slug):
    next = request.GET.get('next')
    variant_id = request.POST.get('variant_id')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)

    cart.add(product, variant_id)
    if next:
        return redirect(next)
    return redirect("shop:cart_page")


def decrease_cart_quantity(request, slug, variant_id):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    cart.add(product, variant_id, -1)
    if next:
        return redirect(next)
    return redirect("shop:cart_page")


def increase_cart_quantity(request, slug, variant_id):
    next = request.GET.get('next')
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    cart.add(product, variant_id)
    if next:
        return redirect(next)
    return redirect("shop:cart_page")


def filter_category(request, slug):
    digit_category = get_object_or_404(DigitCategory, slug=slug)
    products = digit_category.products.all()
    return render(request, 'shop/filter_category.html', {"products": products})