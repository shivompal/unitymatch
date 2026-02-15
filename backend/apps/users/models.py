from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone"]

    def __str__(self):
        return self.email
