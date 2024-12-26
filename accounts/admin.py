from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin', 'date_of_birth', 'pseudoname', 'profile_picture')
    list_filter = ('is_admin', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'date_of_birth', 'profile_picture', 'pseudoname')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'date_of_birth', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'groups')}),
    )

# Register models
admin.site.register(CustomUser, CustomUserAdmin)

