"""Custom user model and manager definitions for the users app."""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Custom manager for User model.

    This manager provides helper methods for creating regular users and
    superusers with email as the unique identifier.
    """

    def create_user(self, email, phone, password=None, **extra_fields):
        """Create and save a regular User with the given email and phone."""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        """Create and save a Superuser with the given email and phone."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, phone, password, **extra_fields)


class User(AbstractUser):
    """Custom user model that uses email as the unique identifier."""

    # Remove the username field from the inherited AbstractUser model.
    username = None

    # Use UUIDs for the primary key to avoid sequential numeric IDs.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = UserManager()

    def __str__(self):
        """Return a readable string representation for the user."""
        return self.email
