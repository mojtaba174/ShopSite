from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib import messages
from shop.models import Product
from .models import Comment
from .forms import CommentForm


def add_comment(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX check
                return JsonResponse({
                    'user': comment.user.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                })

            messages.success(request, "نظر شما ثبت شد.")
            return redirect('shop:detail_page', slug=product.slug)

    comments = product.comments.filter(approved=True).order_by('-created_at')
    form = CommentForm()
    context = {'form': form, 'comments': comments, 'product': product}
    return render(request, 'shop/detail_page.html', context)
