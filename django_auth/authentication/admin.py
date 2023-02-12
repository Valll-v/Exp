from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from authentication.models import UserCreateCode, ActivityCategory


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'phone_number', 'firstname', 'lastname', 'photo', 'last_seen')
    list_filter = ()
    ordering = ()
    fieldsets = (
        (None, {'fields': (
            'phone_number',
            'firstname',
            'lastname',
            'photo'
        )}),
    )
    search_fields = ('phone_number', 'username', 'last_seen')

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(UserCreateCode)
admin.site.register(ActivityCategory)
