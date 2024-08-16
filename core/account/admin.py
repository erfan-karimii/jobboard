from django.contrib import admin
from .models import User, UserProfile,Role
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "role","is_superuser")
    list_filter = (
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
                    "role"                    
                ),
            },
        ),
        ("group permissions", {"fields": ("groups", "user_permissions")}),
        ("date", {"fields": ("last_login",)}),
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
                    "role",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)

admin.site.register(Role)