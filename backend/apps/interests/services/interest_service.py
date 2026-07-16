from django.db import transaction
from django.utils import timezone
from apps.matches.models import Match
from apps.matches.services.match_service import create_chat_room_for_match
from apps.interests.models import InterestStatus


def accept_interest(interest):
    """
    Accept interest and create Match + ChatRoom.
    Safe and idempotent.
    """

    with transaction.atomic():
        if interest.status != InterestStatus.PENDING:
            return interest

        # Update status
        interest.status = InterestStatus.ACCEPTED
        interest.rejection_reason_code = ""
        interest.last_action_at = timezone.now()
        interest.save(
            update_fields=["status", "rejection_reason_code", "last_action_at"]
        )

        # Ensure consistent ordering
        profile1, profile2 = sorted(
            [interest.sender, interest.receiver], key=lambda p: str(p.id)
        )

        # match, created = Match.objects.get_or_create(
        match, _ = Match.objects.get_or_create(profile1=profile1, profile2=profile2)

        create_chat_room_for_match(match)

        return interest
