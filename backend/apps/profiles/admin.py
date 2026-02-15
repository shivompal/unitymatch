from django.contrib import admin
from .models import Profile, ProfilePhoto


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "gender", "religion", "is_active")
    search_fields = ("full_name", "religion", "caste", "city")
    list_filter = ("gender", "religion", "is_active")


@admin.register(ProfilePhoto)
class ProfilePhotoAdmin(admin.ModelAdmin):
    list_display = ("profile", "is_primary", "moderation_status", "created_at")
    list_filter = ("moderation_status", "is_primary")
