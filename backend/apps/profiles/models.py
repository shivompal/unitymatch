import uuid
from django.db import models
from django.conf import settings


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles"
    )

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)

    date_of_birth = models.DateField()

    marital_status = models.CharField(max_length=30)
    children_status = models.CharField(max_length=30)

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

    is_active = models.BooleanField(default=True)
    is_soft_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
