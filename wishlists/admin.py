from django.contrib import admin
from .models import Wishlist, WishlistItem
from django.contrib.auth import get_user_model
from groups.models import Group  # Assuming your Group model is in a different app

# Customizing the admin interface for Wishlist model
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'visibility', 'category', 'group', 'created_at')
    search_fields = ('title', 'user__username', 'group__name', 'category')
    list_filter = ('visibility', 'category', 'group')
    ordering = ('created_at',)
    fields = ('title', 'user', 'description', 'visibility', 'group', 'category', 'created_at')
    readonly_fields = ('created_at',)  # Make 'created_at' field readonly in the admin panel

    # You can add custom form logic or custom save behavior if needed

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'wishlist', 'price_range', 'url', 'bought', 'image')
    search_fields = ('name', 'wishlist__title', 'price_range')
    list_filter = ('price_range', 'bought', 'wishlist__category')
    ordering = ('wishlist__title',)
    fields = ('wishlist', 'name', 'description', 'price_range', 'url', 'image', 'bought')

    def save_model(self, request, obj, form, change):
        # Custom save logic, if needed, e.g., automatically setting fields
        super().save_model(request, obj, form, change)

# Register the models with the admin interface
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)
