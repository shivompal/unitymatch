from django.contrib import admin
from .models import Interest, InterestStatus
from .services.interest_service import accept_interest


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("sender__full_name", "receiver__full_name")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.status == InterestStatus.ACCEPTED:
            accept_interest(obj)
