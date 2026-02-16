from django.contrib import admin
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("profile1", "profile2", "is_active", "matched_at")
    list_filter = ("is_active",)
