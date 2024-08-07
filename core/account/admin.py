from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_superuser", "is_active",)
    list_filter = (
        "email",
        "is_superuser",
        "is_active",
    )
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "Authentications",
            {
                "fields": ("email",),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                )
            },
        ),
        ("group permissions", {"fields": ("groups", "user_permissions")}),
        ("date", {"fields": ("last_login",)}),
        ("Token", {"fields": ("Token",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)

