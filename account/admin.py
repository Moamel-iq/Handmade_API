from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.forms import UserAdminChangeForm
from commerce.admin import User
from account.models import *


class EmailAccountAdmin(BaseUserAdmin):
    form = UserAdminChangeForm

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'phone_number', 'address1', 'address2', 'company_name',
            'company_website')}),
        ('Permissions',
         {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_verified', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(EmailAccount, EmailAccountAdmin)
