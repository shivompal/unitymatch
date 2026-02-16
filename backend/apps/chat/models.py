import uuid
from django.db import models
from apps.matches.models import Match


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    match = models.OneToOneField(
        Match, on_delete=models.CASCADE, related_name="chat_room"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom for {self.match}"
