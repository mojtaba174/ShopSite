from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from shop.models import Product


@require_POST
@login_required
def add_comment(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.product = product
        comment.save()
        return JsonResponse({
            'status': 'ok',
            'username': request.user.username,
            'text': comment.text,
            'rating': comment.rating,
            'is_buyer': comment.is_buyer(),
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
        })
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
