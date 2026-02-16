from apps.chat.models import ChatRoom


def create_chat_room_for_match(match):
    """
    Create chat room when a match is created.
    Safe to call multiple times.
    """
    ChatRoom.objects.get_or_create(match=match)
