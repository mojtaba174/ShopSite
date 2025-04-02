from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from cart.classes.cart import Cart
from shop.models import ProductVariant, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import CartItem
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def cart_page(request):
    if request.user.is_authenticated:
        cart = request.user.cart_item.all()
    else:
        cart = Cart(request)
    return render(request, 'cart/cart_page.html', context={'cart': cart})


def add_to_cart(request, slug):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        next_url = request.POST.get('next')
        variant_id = request.POST.get('variant_id')

        try:
            variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'محصول یافت نشد'}, status=404)

        response_data = {}

        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=variant.product,
                variant=variant,
                defaults={
                    'quantity': 1,
                    'total_price': variant.price
                }
            )

            if not created:
                if variant.quantity > cart_item.quantity:
                    cart_item.quantity += 1
                cart_item.total_price = cart_item.quantity * variant.price
                cart_item.save()
                response_data['action'] = 'increase'
                response_data['quantity'] = cart_item.quantity
                response_data['total_price'] = cart_item.total_price
            else:
                response_data['action'] = 'add'
        else:
            cart = Cart(request)
            cart.add(variant.product, variant_id)
            response_data['action'] = 'add'

        response_data['success'] = True
        response_data['message'] = 'محصول به سبد خرید اضافه شد'
        response_data['next_url'] = next_url if next_url else None
        response_data['cart_count'] = get_cart_count(request)

        return JsonResponse(response_data)

    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'}, status=400)


def get_cart_count(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user).count()
    else:
        cart = Cart(request)
        return len(cart.cart)


def decrease_cart_quantity(request, variant_id):
    if request.method == "POST":
        variant = get_object_or_404(ProductVariant, id=variant_id)
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, variant=variant).first()
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.total_price = cart_item.quantity * variant.price
                    cart_item.save()
                    return JsonResponse({"quantity": cart_item.quantity, "total_price": cart_item.total_price})
                else:
                    cart_item.delete()
                    return JsonResponse({"quantity": 0, "total_price": 0})
        else:
            cart = Cart(request)
            cart.add(variant.product, variant.id, -1)
            new_quantity = cart.cart[f'{variant.product.id}-{variant_id}']['quantity']
            return JsonResponse({"quantity": new_quantity, "total_price": new_quantity * variant.price})

    return JsonResponse({"error": "Invalid request"}, status=400)


def increase_cart_quantity(request, variant_id):
    if request.method == "POST":
        variant = get_object_or_404(ProductVariant, id=variant_id)
        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(user=request.user, variant=variant, defaults={"quantity": 0, "total_price": 0})
            if variant.quantity > cart_item.quantity:
                cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * variant.price
            cart_item.save()
            return JsonResponse({"quantity": cart_item.quantity, "total_price": cart_item.total_price})
        else:
            cart = Cart(request)
            cart.add(variant.product, variant.id, 1)
            new_quantity = cart.cart[f'{variant.product.id}-{variant_id}']['quantity']
            return JsonResponse({"quantity": new_quantity, "total_price": new_quantity * variant.price})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
@api_view(['POST'])
def confirm(request):
    user = request.user
    items = request.data.get('items', [])

    if not items:
        return Response({"error": "سبد خرید خالی است!"}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        order = Order.objects.create(user=user, total_price=0)

        total_price = 0
        order_items = []

        for item in items:
            variant = get_object_or_404(ProductVariant, id=item['variant_id'])
            quantity = item.get('quantity', 1)
            price = variant.price

            order_items.append(OrderItem(order=order, variant=variant, quantity=quantity, price=price))
            total_price += price * quantity

        OrderItem.objects.bulk_create(order_items)
        order.total_price = total_price
        order.save()

    return Response({"message": "سفارش شما با موفقیت ثبت شد!", "order_id": order.id}, status=status.HTTP_201_CREATED)