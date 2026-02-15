import uuid
from django.db import models
from django.conf import settings


class GenderChoices(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class MaritalStatusChoices(models.TextChoices):
    NEVER_MARRIED = "never_married", "Never Married"
    DIVORCED = "divorced", "Divorced"
    WIDOWED = "widowed", "Widowed"


class ChildrenStatusChoices(models.TextChoices):
    NONE = "none", "No Children"
    HAS_CHILDREN = "has_children", "Has Children"


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles"
    )

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GenderChoices.choices)

    date_of_birth = models.DateField()

    marital_status = models.CharField(
        max_length=30, choices=MaritalStatusChoices.choices
    )

    children_status = models.CharField(
        max_length=30, choices=ChildrenStatusChoices.choices
    )

    religion = models.CharField(max_length=100)
    caste = models.CharField(max_length=100, blank=True)
    sub_caste = models.CharField(max_length=100, blank=True)

    mother_tongue = models.CharField(max_length=100)

    height_cm = models.PositiveIntegerField()

    education = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    annual_income = models.PositiveIntegerField(null=True, blank=True)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    bio = models.TextField(blank=True)

    rashi = models.CharField(max_length=100, blank=True)
    manglik = models.BooleanField(default=False)

    anonymous_mode_enabled = models.BooleanField(default=False)
    profile_visibility = models.CharField(max_length=20, default="public")

    is_active = models.BooleanField(default=True)
    is_soft_deleted = models.BooleanField(default=False)
    soft_deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["gender"]),
            models.Index(fields=["date_of_birth"]),
            models.Index(fields=["religion"]),
            models.Index(fields=["caste"]),
            models.Index(fields=["country", "state", "city"]),
            models.Index(fields=["is_active", "is_soft_deleted"]),
        ]


class PhotoModerationStatus(models.TextChoices):
    UPLOADED = "uploaded", "Uploaded"
    UNDER_REVIEW = "under_review", "Under Review"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class ProfilePhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="photos"
    )

    image = models.ImageField(upload_to="profile_photos/")

    is_primary = models.BooleanField(default=False)

    moderation_status = models.CharField(
        max_length=20,
        choices=PhotoModerationStatus.choices,
        default=PhotoModerationStatus.UPLOADED,
    )

    moderation_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.profile.full_name}"
