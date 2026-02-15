import uuid
from django.db import models
from apps.profiles.models import Profile


class InterestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    WITHDRAWN = "withdrawn", "Withdrawn"


class Interest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="sent_interests"
    )

    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="received_interests"
    )

    status = models.CharField(
        max_length=20, choices=InterestStatus.choices, default=InterestStatus.PENDING
    )

    rejection_reason_code = models.CharField(max_length=50, blank=True)

    last_action_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")
        indexes = [
            models.Index(fields=["sender"]),
            models.Index(fields=["receiver"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
