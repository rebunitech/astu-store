from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from auser.models import (Department, DepartmentRepresentative, School,
                          SchoolRepresentative, StoreKeeper, User)


@admin.register(DepartmentRepresentative)
class DepartmentAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "department",
                    "username",
                    "email",
                    "sex",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    exclude = ["date_joined"]


@admin.register(SchoolRepresentative)
class SchoolAdmin(UserAdmin):
    pass


@admin.register(StoreKeeper)
class StoreKeeperAdmin(UserAdmin):
    pass


admin.site.register(Department)
admin.site.register(School)
