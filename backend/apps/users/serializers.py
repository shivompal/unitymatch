"""Serializers for the users app."""

from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration requests."""

    # Ensure the password is only written and never returned in responses.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "phone", "password"]

    def create(self, validated_data):
        """Create a new User instance using the validated registration data."""
        return User.objects.create_user(**validated_data)
