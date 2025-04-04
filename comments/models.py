from django.db import models
from django.conf import settings
from shop.models import Product
from django.contrib.auth.models import User


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def is_buyer(self):
        return self.user.orders.filter(status='ثبت شد').exists()

    def __str__(self):
        return f'{self.user.username} - {self.product} - {self.rating} ⭐️'
