from django.contrib import admin
from . import models
from comments.models import Comment


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1


class ProductTechnical(admin.TabularInline):
    model = models.ProductTechnical
    extra = 1


class ProductVariant(admin.TabularInline):
    model = models.ProductVariant
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductTechnical, ProductVariant, CommentInline]
    prepopulated_fields = {"slug": ("title",)}


class UserCommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class OrderItem(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItem]


admin.site.register(models.DigitCategory)
admin.site.register(models.ProductVariant)
admin.site.register(models.Color)
admin.site.register(models.ProductImage)
admin.site.register(models.Brand)
