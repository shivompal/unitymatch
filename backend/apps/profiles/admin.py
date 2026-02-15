from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "gender", "religion", "is_active")
    search_fields = ("full_name", "religion", "caste", "city")
    list_filter = ("gender", "religion", "is_active")
