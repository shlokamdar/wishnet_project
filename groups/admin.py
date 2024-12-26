from django.contrib import admin
from .models import Group, Profile

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'budget_limit', 'total_price', 'is_budget_exceeded', 'created_at', 'secret_santa_assigned', 'join_code')
    list_filter = ('secret_santa_assigned', 'created_at')
    
    # Fields that are readonly in the admin panel
    readonly_fields = ('join_code', 'is_budget_exceeded', 'created_at', 'updated_at', 'secret_santa_assigned')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pseudoname', 'secret_santa_assigned_to')
    search_fields = ('user__username', 'pseudoname')
    readonly_fields = ('user', 'secret_santa_assigned_to')
    fieldsets = (
        (None, {
            'fields': ('user', 'pseudoname', 'secret_santa_assigned_to')
        }),
    )


# Register models with custom admin interfaces
admin.site.register(Group, GroupAdmin)
admin.site.register(Profile, ProfileAdmin)
