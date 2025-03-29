from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(verbose_name='آیکون', default="static/default.png")

    def __str__(self):
        return self.name


class DigitCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='دسته بندی')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hex_code = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(DigitCategory, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(max_length=500)
    slug = models.SlugField(default="", null=False, unique=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'image for {self.product}'


class ProductTechnical(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='technical')
    title = models.CharField(max_length=200)
    value = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ProductVariant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color,on_delete=models.CASCADE, related_name='variants')
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [('product', 'color')]

    def __str__(self):
        return f"{self.product.title} - {self.color.name}"


class Comment(models.Model):

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    content = models.TextField(verbose_name="comment here")
    rating = models.PositiveSmallIntegerField(
        verbose_name="rate",
        choices=[(i, i) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.product.title} - {self.rating} ⭐️'
