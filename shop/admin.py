from django.contrib import admin
from . import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1


class ProductTechnical(admin.TabularInline):
    model = models.ProductTechnical
    extra = 1


class ProductVariant(admin.TabularInline):
    model = models.ProductVariant
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductTechnical, ProductVariant]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(models.DigitCategory)
admin.site.register(models.ProductVariant)
admin.site.register(models.Color)
admin.site.register(models.ProductImage)
admin.site.register(models.Brand)
