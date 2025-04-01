from django.shortcuts import render, get_object_or_404, redirect
from .models import DigitCategory
from django.contrib import messages
from shop.models import Product
from .forms import CommentForm


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





def filter_category(request, slug):
    digit_category = get_object_or_404(DigitCategory, slug=slug)
    products = digit_category.products.all()
    return render(request, 'shop/filter_category.html', {"products": products})


def search_results(request):
    value = request.GET.get('value')
    products = Product.objects.filter(title__contains=value)
    return render(request, 'shop/filter_category.html', {'products': products})


def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    return render(request, 'contact_us.html')