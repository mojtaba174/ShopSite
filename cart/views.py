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
from .serializer import CartItemSerializer


def cart_page(request):
    if request.user.is_authenticated:
        cart = request.user.cart_item.all()
    else:
        cart = Cart(request)
    return render(request, 'cart/cart_page.html', context={'cart': cart, 'is_authenticated': request.user.is_authenticated})


def add_to_cart(request):
    if request.method == "POST":
        variant_id = request.POST.get("variant_id")
        variant = get_object_or_404(ProductVariant, id=variant_id)

        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user, variant=variant,
                defaults={"quantity": 0, "total_price": 0}
            )

            if cart_item.quantity < variant.quantity:
                cart_item.quantity += 1
                cart_item.total_price = cart_item.quantity * variant.price
                cart_item.save()
                return JsonResponse({
                    "success": True,
                    "quantity": cart_item.quantity,
                    "total_price": cart_item.total_price,
                    "cart_count": CartItem.objects.filter(user=request.user).count()
                })
            else:
                return JsonResponse({"success": False, "message": "موجودی کافی نیست"}, status=400)

        else:
            cart = Cart(request)
            if f"{variant.product.id}-{variant_id}" in cart.cart.keys():
                current_quantity = cart.cart[f"{variant.product.id}-{variant_id}"]['quantity']
            else:
                current_quantity = 0

            if current_quantity < variant.quantity:
                cart.add(variant.product, variant.id, 1)
                new_quantity = cart.cart[f"{variant.product.id}-{variant_id}"]['quantity']
                return JsonResponse({
                    "success": True,
                    "quantity": new_quantity,
                    "total_price": new_quantity * variant.price,
                    "cart_count": len(cart.cart.keys())
                })
            else:
                return JsonResponse({"success": False, "message": "موجودی کافی نیست"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


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
            variant = get_object_or_404(ProductVariant, id=item['variant'])
            quantity = item.get('quantity', 1)
            price = variant.price

            order_items.append(OrderItem(order=order, variant=variant, quantity=quantity, price=price))
            total_price += price * quantity

        OrderItem.objects.bulk_create(order_items)
        order.total_price = total_price
        order.save()

    return Response({"message": "سفارش شما با موفقیت ثبت شد!", "order_id": order.id}, status=status.HTTP_201_CREATED)


@login_required
def get_cart_items(request):
    items = CartItem.objects.filter(user=request.user)
    data = CartItemSerializer(items, many=True).data
    return JsonResponse({'items': data})
