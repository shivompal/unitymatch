import uuid
from django.db import models
from apps.profiles.models import Profile


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    profile1 = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="matches_as_profile1"
    )

    profile2 = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="matches_as_profile2"
    )

    is_active = models.BooleanField(default=True)

    ended_by = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="ended_matches",
    )

    ended_at = models.DateTimeField(null=True, blank=True)

    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile1", "profile2"], name="unique_match_pair"
            )
        ]
        indexes = [
            models.Index(fields=["profile1"]),
            models.Index(fields=["profile2"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.profile1} ❤️ {self.profile2}"
