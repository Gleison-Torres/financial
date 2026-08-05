from django.contrib import admin
from django.contrib.auth.models import User


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'username', 'is_active', 'is_staff')