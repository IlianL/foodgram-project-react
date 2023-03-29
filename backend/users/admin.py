from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = (
        'is_active', 'username', 'first_name', 'last_name', 'email',
    )
    search_fields = ('username', 'email',)
    list_filter = ('first_name', 'email',)
    ordering = ('username', 'id',)
    empty_value_display = '-пусто-'
