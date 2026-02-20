from rest_framework import serializers
from apps.profiles.models import Profile


class DiscoveryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "full_name",
            "gender",
            "date_of_birth",
            "religion",
            "mother_tongue",
            "city",
            "state",
            "country",
        ]
