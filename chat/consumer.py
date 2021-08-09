# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, SyncConsumer, AsyncWebsocketConsumer, \
    AsyncJsonWebsocketConsumer, AsyncConsumer
from channels.db import database_sync_to_async
from .models import Message, Chat
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer
from django.db.models import Q

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.receiver = self.scope["url_route"]["kwargs"]["username"]
        self.user = self.scope['user']
        self.chat = await self.get_chat_object(sender=self.user, receiver=self.receiver)

        await self.channel_layer.group_add(str(self.chat.id).replace("-", ""), self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })

        print(f'[{self.user}] You are connected to the channel {self.channel_name}')

    async def websocket_receive(self, event):

        print(f'[{self.user}] Recieved message {event["text"]}')

        # save it in the database
        await self.save_message(username=self.user, message=event['text'])
        await self.channel_layer.group_send(str(self.chat.id).replace("-", ""), {
            "type": "send.message",
            "text": event["text"],
        })

    async def websocket_disconnect(self, close_code):
        print(f'[{self.user}] Disconnected with code {close_code}')
        await self.channel_layer.group_discard(str(self.chat.id).replace("-", ""), self.channel_name)

    async def send_message(self, event):
        print(f'[{self.user}] Message sent {event["text"]}')

        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })

    @database_sync_to_async
    def save_message(self, username, message, ):
        return Message.objects.create(author=username, message=message, chat_id=self.chat)

    @database_sync_to_async
    def get_chat_object(self, sender, receiver):
        try:
            chat = Chat.objects.get(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
            chat.save()
        except ObjectDoesNotExist:
            chat = Chat.objects.create(sender=sender, receiver=receiver)
        return chat
