from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 'position']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'position')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'position',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )
    
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Wojewodztwo)
admin.site.register(models.Powiat)
admin.site.register(models.Kontrahent)
admin.site.register(models.Typ)
admin.site.register(models.Status)
admin.site.register(models.RodzajZadania)
admin.site.register(models.Specjalista)
admin.site.register(models.Branza)
admin.site.register(models.RodzajUprawnien)
admin.site.register(models.ObszarDzialania)
admin.site.register(models.Zadanie)
admin.site.register(models.SpecjalistaZadania)
admin.site.register(models.SpecjalistaBranza)

