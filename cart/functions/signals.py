from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from ..classes.cart import Cart
from ..models import CartItem


@receiver(user_logged_in)
def transfer_cart_items(sender, request, user, **kwargs):
    session_cart = Cart(request)

    for item in session_cart:
        CartItem.objects.update_or_create(
            user=user,
            variant=item["variant"],
            defaults={"quantity": item["quantity"], "total_price": item["total_price"]},
        )

    session_cart.clear()
