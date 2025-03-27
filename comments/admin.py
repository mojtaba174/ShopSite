from django.contrib import admin

from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'content', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username', 'content')

    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
