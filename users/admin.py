from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('user_name', 'employee_id')
    list_filter = ('user_name', 'employee_id', 'is_active', 'is_staff','is_admin')
    ordering = ('-start_date',)
    list_display = ('user_name', 'employee_id',
                    'is_active', 'is_staff','is_admin')
    fieldsets = (
        (None, {'fields': ('user_name', 'employee_id',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'employee_id', 'password1', 'password2', 'is_active', 'is_staff','is_admin')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
