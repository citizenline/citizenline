from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.site_header = 'Citizenline admin'
admin.site.unregister(User)


class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )

admin.site.register(User, MyUserAdmin)