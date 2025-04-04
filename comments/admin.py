from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('product', 'user', 'rating', 'created_at')
    search_fields = ('user__username', 'product__title', 'content')
    ordering = ('-created_at',)





