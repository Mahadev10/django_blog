from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.
@admin.register(models.UserProfile)
class UserProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "profile_photo",
                ),
            },
        ),
    )
    list_display = ('id','username')