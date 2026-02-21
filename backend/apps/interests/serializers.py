from rest_framework import serializers
from apps.profiles.models import Profile
from .models import Interest, InterestStatus


class InterestActorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "full_name"]


class InterestListSerializer(serializers.ModelSerializer):
    sender = InterestActorProfileSerializer(read_only=True)
    receiver = InterestActorProfileSerializer(read_only=True)

    class Meta:
        model = Interest
        fields = [
            "id",
            "sender",
            "receiver",
            "status",
            "rejection_reason_code",
            "last_action_at",
            "created_at",
        ]


class SendInterestSerializer(serializers.Serializer):
    sender_profile_id = serializers.UUIDField()
    receiver_profile_id = serializers.UUIDField()

    def validate(self, attrs):
        request = self.context["request"]
        sender_profile_id = attrs["sender_profile_id"]
        receiver_profile_id = attrs["receiver_profile_id"]

        try:
            sender_profile = Profile.objects.get(id=sender_profile_id)
        except Profile.DoesNotExist:
            raise serializers.ValidationError({"sender_profile_id": "Invalid profile."})

        try:
            receiver_profile = Profile.objects.get(id=receiver_profile_id)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {"receiver_profile_id": "Invalid profile."}
            )

        if sender_profile.user_id != request.user.id:
            raise serializers.ValidationError(
                {"sender_profile_id": "You can send interest only from your own profile."}
            )

        if sender_profile.id == receiver_profile.id:
            raise serializers.ValidationError(
                {"receiver_profile_id": "You cannot send interest to your own profile."}
            )

        if Interest.objects.filter(
            sender=sender_profile, receiver=receiver_profile
        ).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["Interest already exists between these profiles."]}
            )

        attrs["sender_profile"] = sender_profile
        attrs["receiver_profile"] = receiver_profile
        return attrs

    def create(self, validated_data):
        return Interest.objects.create(
            sender=validated_data["sender_profile"],
            receiver=validated_data["receiver_profile"],
            status=InterestStatus.PENDING,
        )


class RejectInterestSerializer(serializers.Serializer):
    rejection_reason_code = serializers.CharField(required=False, allow_blank=True)


class InterestActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ["id", "status", "rejection_reason_code", "last_action_at", "created_at"]
