from django.db import transaction
from apps.matches.models import Match
from apps.matches.services.match_service import create_chat_room_for_match


def accept_interest(interest):
    """
    Create Match + ChatRoom when interest is accepted.
    Safe to call multiple times.
    """

    with transaction.atomic():
        # Ensure consistent ordering
        profile1, profile2 = sorted(
            [interest.sender, interest.receiver], key=lambda p: str(p.id)
        )

        match, created = Match.objects.get_or_create(
            profile1=profile1, profile2=profile2
        )

        # Always ensure chat room exists
        create_chat_room_for_match(match)
