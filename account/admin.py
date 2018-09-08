from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    fieldsets = (
            ('User Profile', {'fields': ('name', 'following', 'follower', 'website', 'bio')}),
    ) + AuthUserAdmin.fieldsets
    list_display = ('id', 'username', 'name', 'is_superuser', 'website', 'bio')
    search_fields = ['name']
    list_display_links = ('username', )
