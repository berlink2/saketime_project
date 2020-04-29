from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


# Register your models

class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ('username', "first_name", "last_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),)
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),)
    list_display = (
        "id",
        "email",
        'username',
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name", 'username')
    ordering = ("email",)


admin.site.register(User, UserAdmin)