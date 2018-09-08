from django.contrib import admin
from .models import Like, Comment, Image


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'image',
        'created_date',
        'modified_date',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'message',
        'creator',
        'image',
        'created_date',
        'modified_date',
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'location',
        'caption',
        'file',
        'creator',
        'created_date',
        'modified_date',
    )

    list_display_links = ('location', 'caption', )

    search_fields = ('location', 'caption', )

    list_filter = ('location', 'creator', )
