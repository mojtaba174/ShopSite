from django.db import models
from django.contrib.auth.models import User
from shop.models import Product, ProductVariant


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.quantity})"
