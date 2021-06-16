from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class Admin(UserAdmin):
    list_display = ('full_name', 'email', 'is_staff',
                    'total_hours', 'is_active')
    search_fields = ('full_name', 'email')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('full_name', 'email')


admin.site.register(User, Admin)
