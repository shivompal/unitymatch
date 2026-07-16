from rest_framework import serializers
from .models import Profile, ProfilePhoto


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["user"]


class ProfilePhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = ["id", "profile", "image", "is_primary", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_profile(self, profile):
        request = self.context.get("request")
        if request and profile.user != request.user:
            raise serializers.ValidationError(
                "You can upload photos only for your own profiles."
            )
        return profile


class ProfilePhotoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = [
            "id",
            "profile",
            "image",
            "is_primary",
            "moderation_status",
            "created_at",
        ]
