from django.contrib import admin
from .models import User, Applications


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')


@admin.register(Applications)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'status', 'category')
