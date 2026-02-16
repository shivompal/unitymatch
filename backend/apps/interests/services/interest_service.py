from django.db import transaction
from apps.matches.models import Match


def accept_interest(interest):
    """
    Create a Match when an interest is accepted.
    Safe to call multiple times (idempotent).
    """

    with transaction.atomic():
        # Ensure consistent ordering to avoid duplicate match pairs
        profile1, profile2 = sorted(
            [interest.sender, interest.receiver], key=lambda p: str(p.id)
        )

        Match.objects.get_or_create(profile1=profile1, profile2=profile2)
