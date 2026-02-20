from datetime import date, timedelta
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.profiles.models import Profile
from apps.interests.models import Interest
from apps.matches.models import Match
from .serializers import DiscoveryProfileSerializer


class DiscoveryView(ListAPIView):
    serializer_class = DiscoveryProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # My profiles
        my_profiles = Profile.objects.filter(user=user)

        # Exclude user's own profiles
        queryset = Profile.objects.exclude(user=user)

        # ---- Exclude already interacted profiles ----

        # Profiles I sent interest to
        sent_interest_profiles = Interest.objects.filter(
            sender__in=my_profiles
        ).values_list("receiver_id", flat=True)

        # Profiles who sent interest to me
        received_interest_profiles = Interest.objects.filter(
            receiver__in=my_profiles
        ).values_list("sender_id", flat=True)

        # Profiles already matched with me
        matched_profiles = Match.objects.filter(profile1__in=my_profiles).values_list(
            "profile2_id", flat=True
        )

        matched_profiles_reverse = Match.objects.filter(
            profile2__in=my_profiles
        ).values_list("profile1_id", flat=True)

        excluded_ids = set(
            list(sent_interest_profiles)
            + list(received_interest_profiles)
            + list(matched_profiles)
            + list(matched_profiles_reverse)
        )

        queryset = queryset.exclude(id__in=excluded_ids)

        # ---- Gender filter ----
        gender = self.request.query_params.get("gender")
        if gender:
            queryset = queryset.filter(gender=gender)

        # ---- Age filters ----
        min_age = self.request.query_params.get("min_age")
        max_age = self.request.query_params.get("max_age")

        today = date.today()

        if min_age:
            max_dob = today - timedelta(days=int(min_age) * 365)
            queryset = queryset.filter(date_of_birth__lte=max_dob)

        if max_age:
            min_dob = today - timedelta(days=int(max_age) * 365)
            queryset = queryset.filter(date_of_birth__gte=min_dob)

        # ---- Location filters ----
        country = self.request.query_params.get("country")
        state = self.request.query_params.get("state")
        city = self.request.query_params.get("city")

        if country:
            queryset = queryset.filter(country__iexact=country)

        if state:
            queryset = queryset.filter(state__iexact=state)

        if city:
            queryset = queryset.filter(city__iexact=city)

        return queryset
