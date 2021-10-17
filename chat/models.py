from django.db import models
from user.models import User
import uuid

class Chat(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_first = models.OneToOneField(User, related_name="user_first_chat", on_delete=models.CASCADE, default='')
    user_second = models.OneToOneField(User, related_name="user_second_chat", on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def last_30_messages(self, chat_id):
        return Message.objects.order_by('-created_at').filter(chat_id=chat_id).all()[:30]


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(User, related_name="user_message", on_delete=models.CASCADE, default='')
    chat_id = models.ForeignKey(Chat, related_name="chat_message", on_delete=models.CASCADE, default='')
    message = models.TextField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChannelModel(models.Model):
    channel_name = models.TextField(max_length=255)
