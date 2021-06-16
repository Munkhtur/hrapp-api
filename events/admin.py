from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Events

# Register your models here.


class Admin(UserAdmin):
    list_display = ('owner', 'content', 'date', 'type')
    search_fields = ('owner', 'content')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('owner', 'date')


admin.site.register(Events, Admin)
