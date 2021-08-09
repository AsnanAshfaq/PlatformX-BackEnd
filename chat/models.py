from django.db import models
from user.models import User
import uuid
from django.db.models import Q


class Chat(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.TextField(max_length=200, default='')
    receiver = models.TextField(max_length=200, default='')
    # sender = models.ForeignKey(User, related_name="user_sender", on_delete=models.CASCADE)
    # reciever = models.OneToOneField(User, related_name="user_reciever", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_30_messages(self, chat_id):
        return Message.objects.order_by('-timestamp').filter(chat_id=chat_id).all()[:30]


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # author = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
    author = models.TextField(max_length=200)
    chat_id = models.ForeignKey(Chat, related_name="chat_messages", on_delete=models.CASCADE, default='')
    message = models.TextField(max_length=255, default="")
    timestamp = models.DateTimeField(auto_now_add=True)