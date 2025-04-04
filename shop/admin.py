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
    # inlines = [ProductImageInline, ProductTechnical, ProductVariant, ]
    inlines = [ProductImageInline, ProductTechnical, ProductVariant, CommentInline]
    prepopulated_fields = {"slug": ("title",)}


class UserCommentInline(admin.TabularInline):
    model = Comment
    extra = 1


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'product', 'rating', 'created_at')
#     list_filter = ('product', 'user', 'rating', 'created_at')
#     search_fields = ('user__username', 'product__title', 'content')
#     ordering = ('-created_at',)


admin.site.register(models.DigitCategory)
admin.site.register(models.ProductVariant)
admin.site.register(models.Color)
admin.site.register(models.ProductImage)
admin.site.register(models.Brand)
admin.site.register(models.Order)