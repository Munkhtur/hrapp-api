from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Attendance
# Register your models here.


class Admin(UserAdmin):
    list_display = ('id', 'name', 'email', 'department', 'clockin',
                    'clockout', 'workhours', 'breakhours', 'status')
    search_fields = ('id', 'name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('id', 'name')


admin.site.register(Attendance, Admin)
