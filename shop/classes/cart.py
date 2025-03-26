class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            if product.quantity >= self.cart[product_id]['quantity'] + quantity > 0:
                self.cart[product_id]['quantity'] += quantity
            elif product.quantity < self.cart[product_id]['quantity'] + quantity:
                self.cart[product_id]['quantity'] = product.quantity
            elif self.cart[product_id]['quantity'] + quantity == 0:
                self.remove(product)
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.save()

    def __iter__(self):
        from ..models import Product
        products_id = self.cart.keys()
        products = Product.objects.filter(id__in=products_id)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            yield item

