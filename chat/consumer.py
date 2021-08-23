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
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.receiver = self.scope["url_route"]["kwargs"]["username"]
        self.user = self.scope['user']

        # if the user is anonymous then close the connection
        if self.user == AnonymousUser():
            print("User is anonymous. Therefore closing the connection")
            await self.websocket_disconnect(close_code=1006)
        else:
            # get the user object for receiver user
            self.receiver = await self.get_receiver_user_object(username=self.receiver)
            # get the user object for sender user
            self.chat = await self.get_chat_object(sender=self.user, receiver=self.receiver)
            await self.channel_layer.group_add(str(self.chat.id).replace("-", ""), self.channel_name)
            await self.send({
                "type": "websocket.accept",
            })

            print(f'[{self.user}] You are connected to the channel {self.channel_name}')

    async def websocket_receive(self, event):

        print(f'[{self.user}] Recieved message {event["text"]}')

        # save it in the database
        self.message = await self.save_message(user=self.user, message=event['text'])
        await self.channel_layer.group_send(str(self.chat.id).replace("-", ""), {
            "type": "send.message",
            "text": event["text"],
        })

    async def websocket_disconnect(self, close_code):
        print(f'[{self.user}] Disconnected with code {close_code}')
        if self.user != AnonymousUser():
            await self.channel_layer.group_discard(str(self.chat.id).replace("-", ""), self.channel_name)

    async def send_message(self, event):
        print(f'[{self.user}] Message sent {event["text"]}')

        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    @database_sync_to_async
    def save_message(self, user, message):
        return Message.objects.create(author=user, message=message, chat_id=self.chat)

    @database_sync_to_async
    def get_receiver_user_object(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def get_chat_object(self, sender, receiver):
        try:
            chat = Chat.objects.get(
                Q(user_first=sender, user_second=receiver) | Q(user_first=receiver, user_second=sender))
            # chat.save()
        except Chat.DoesNotExist:
            chat = Chat.objects.create(user_first=sender, user_second=receiver)
        return chat
