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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='variants')
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [('product', 'color')]

    def __str__(self):
        return f"{self.product.title} - {self.color.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('ثبت شد', 'ثبت شد'),
        ('در حال آماده سازی سفارش', 'در حال آماده سازی سفارش'),
        ('در حال ارسال', 'در حال ارسال'),
        ('تحویل داده شد', 'تحویل داده شد'),
        ('کنسل شد', 'کنسل شد'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='ثبت شد')
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderItems')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='productVariant')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.title} in Order {self.order.id}"
