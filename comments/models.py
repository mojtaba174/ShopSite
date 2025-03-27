from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from shop.models import Product


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.product.title[:20]}'
