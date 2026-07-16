import uuid
from django.db import models
from apps.matches.models import Match
from apps.profiles.models import Profile


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    match = models.OneToOneField(
        Match, on_delete=models.CASCADE, related_name="chat_room"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom for {self.match}"


class MessageType(models.TextChoices):
    TEXT = "text", "Text"
    IMAGE = "image", "Image"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )

    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="sent_messages"
    )

    content = models.TextField(blank=True)

    message_type = models.CharField(
        max_length=10, choices=MessageType.choices, default=MessageType.TEXT
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["chat_room", "created_at"]),
        ]

    def __str__(self):
        return f"Message from {self.sender}"
