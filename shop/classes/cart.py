from django.shortcuts import get_object_or_404
from ..models import Product, ProductVariant


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, variant_id, quantity=1):
        product_id = str(product.id)
        variant = get_object_or_404(ProductVariant, id=variant_id)

        cart_key = f"{product_id}-{variant_id}"

        if cart_key in self.cart:
            if variant.quantity >= self.cart[cart_key]['quantity'] + quantity > 0:
                self.cart[cart_key]['quantity'] += quantity
            elif variant.quantity < self.cart[cart_key]['quantity'] + quantity:
                self.cart[cart_key]['quantity'] = variant.quantity
            elif self.cart[cart_key]['quantity'] + quantity == 0:
                self.remove(product_id, variant_id)
        else:
            self.cart[cart_key] = {'quantity': quantity, 'price': float(variant.price)}

        self.save()

    def remove(self, product_id, variant_id):
        cart_key = f"{product_id}-{variant_id}"
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.save()

    def __iter__(self):

        cart_items = self.cart.copy()
        product_variant_ids = [key.split("-") for key in cart_items.keys()]

        product_ids = {pid for pid, _ in product_variant_ids}
        variant_ids = {vid for _, vid in product_variant_ids}

        products = Product.objects.filter(id__in=product_ids).prefetch_related('variants')
        variants = ProductVariant.objects.filter(id__in=variant_ids)

        product_map = {str(product.id): product for product in products}
        variant_map = {str(variant.id): variant for variant in variants}

        for key, item in cart_items.items():
            product_id, variant_id = key.split("-")
            product = product_map.get(product_id)
            variant = variant_map.get(variant_id)

            if product and variant:
                item['product'] = product
                item['variant'] = variant
                item['total_price'] = variant.price * item['quantity']
                yield item

    def get_total_price(self):

        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def get_total_quantity(self):

        return sum(item['quantity'] for item in self.cart.values())
