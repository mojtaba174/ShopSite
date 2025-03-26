from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(verbose_name='آیکون', default="static/default.png")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام برند')

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    colors = models.JSONField(default=list)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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
