# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, SyncConsumer, AsyncWebsocketConsumer, \
    AsyncJsonWebsocketConsumer, AsyncConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Chat
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer
from django.db.models import Q
from user.models import User
import json
from uuid import UUID
from user.serializer import UserSerializer


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.receiver = self.scope["url_route"]["kwargs"]["receiver_username"]
        self.sender = self.scope["url_route"]["kwargs"]["sender_username"]

        # get the user object for receiver user
        self.receiver = await self.get_user_object(username=self.receiver)

        # get the user object for sender use
        self.sender = await self.get_user_object(username=self.sender)
        # if the user is anonymous then close the connection

        self.chat = None

        # if sender and receiver are valid users
        if self.sender and self.receiver:

            self.chat = await self.get_chat_object(sender=self.sender, receiver=self.receiver)

            await self.channel_layer.group_add(str(self.chat.id).replace("-", ""), self.channel_name)
            # get the user object for sender user
            await self.send({
                "type": "websocket.accept",
            })
            print(f'[{self.sender}] You are connected to the channel {self.channel_name}')

        else:

            await self.websocket_disconnect(close_code=4123)

    async def websocket_receive(self, event):

        print(f'[{self.sender}] Received message {event["text"]}')

        # save it in the database
        self.message = await self.save_message(user=self.sender, message=event['text'])
        await self.channel_layer.group_send(str(self.chat.id).replace("-", ""), {
            "type": "send.message",
            "text": event["text"],
        })

    async def websocket_disconnect(self, close_code):

        if self.chat:
            # if chat exists then close the chat channel
            await self.channel_layer.group_discard(str(self.chat.id).replace("-", ""), self.channel_name)

        await self.send({
            "type": "websocket.close",
            "code": close_code
        })

        print(f'[{self.sender}] Disconnected with code {close_code}')

    async def send_message(self, event):
        print(f'[{self.sender}] Message sent {event["text"]}')

        # message_id = json.dumps(self.message.id, cls=UUIDEncoder)
        # chat_id = json.dumps(self.message.chat_id.id, cls=UUIDEncoder)
        # timestamp = json.dumps(self.message.timestamp, indent=4, sort_keys=True, default=str)

        message_id = str(self.message.id)
        timestamp = str(self.message.timestamp)
        chat_id = str(self.message.chat_id.id)
        user_name = str(self.sender)
        response = json.dumps({
            'id': message_id,
            'message': self.message.message,
            'timestamp': timestamp,
            'chat_id': chat_id,
            'user_name': user_name
        })

        await self.send({
            "type": "websocket.send",
            "text": response
        })

    @database_sync_to_async
    def save_message(self, user, message):
        return Message.objects.create(author=user, message=message, chat_id=self.chat)

    @database_sync_to_async
    def get_user_object(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            self.websocket_disconnect(4123)
            return None

    @database_sync_to_async
    def get_chat_object(self, sender, receiver):
        try:
            chat = Chat.objects.get(
                Q(user_first=sender, user_second=receiver) | Q(user_first=receiver, user_second=sender))
            # chat.save()
        except Chat.DoesNotExist:
            chat = Chat.objects.create(user_first=sender, user_second=receiver)
        return chat
