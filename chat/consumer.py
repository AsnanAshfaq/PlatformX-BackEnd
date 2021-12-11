# chat/consumers.py
from channels.generic.websocket import AsyncConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Chat, ChannelModel
from django.db.models import Q
from user.models import User, ProfileImage
import json
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self):
        self.receiver = None
        self.sender = None
        self.chat = None
        self.message_object = None

    async def websocket_connect(self, event):
        self.receiver = self.scope["url_route"]["kwargs"]["receiver_username"]
        self.sender = self.scope["url_route"]["kwargs"]["sender_username"]

        # get the user object for receiver user
        self.receiver = await self.get_user_object(username=self.receiver)

        # get the user object for sender use
        self.sender = await self.get_user_object(username=self.sender)
        # if the user is anonymous then close the connection

        # if sender and receiver are valid users
        if self.sender and self.receiver:

            self.chat = await self.get_chat_object(sender=self.sender, receiver=self.receiver)

            await self.channel_layer.group_add(str(self.chat.id).replace("-", ""), self.channel_name)

            # accept the connection

            await self.accept()

            print(f'[{self.sender}] You are connected to the channel {self.channel_name}')
        else:
            await self.websocket_disconnect(close_code=4123)

    async def websocket_receive(self, event):

        print(f'[{self.sender}] Received message {event["text"]}')

        await self.channel_layer.group_send(str(self.chat.id).replace("-", ""), {
            "type": "send.message",
            "text": event["text"],
            "user_id": str(self.sender.id),
            "user_name": str(self.sender.username)
        })

    async def send_message(self, event):
        print(f'[{self.sender}] Message sent {event["text"]}')

        # save it in the database
        self.message_object = await self.save_message(user=self.sender, message=event['text'])

        profile_image = await self.get_receiver_profile_image()
        message_id = str(self.message_object.id)
        message = self.message_object.message
        created_at = str(self.message_object.created_at)

        # user id is coming from event dict
        response = json.dumps({
            'id': message_id,
            'user_id': event['user_id'],
            'message': message,
            'created_at': created_at,
            'user_name': event['user_name'],
            "profile_image": str(profile_image)
        })

        await self.send(response)

    async def websocket_disconnect(self, close_code):

        if self.chat:
            # if chat exists then close the chat channel
            await self.channel_layer.group_discard(str(self.chat.id).replace("-", ""), self.channel_name)

        await self.send({
            "type": "websocket.close",
            "code": close_code
        })

        raise StopConsumer()

        print(f'[{self.sender}] Disconnected with code {close_code}')

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
        print("Sender is", sender, " receiver is", receiver)
        try:
            chat = Chat.objects.get(
                Q(user_first=sender, user_second=receiver) | Q(user_first=receiver, user_second=sender))
            # chat.save()
        except Chat.DoesNotExist:
            chat = Chat.objects.create(user_first=sender, user_second=receiver)
        return chat

    @database_sync_to_async
    def get_channel_object(self, channel_name):
        try:
            return ChannelModel.objects.filter(channel_name=channel_name)
        except ChannelModel.DoesNotExist:
            return None

    @database_sync_to_async
    def save_channel_object(self, channel_name):
        return ChannelModel.objects.create(channel_name=channel_name)

    @database_sync_to_async
    def delete_channel_object(self, channel_name):
        ChannelModel.objects.filter(channel_name=channel_name).delete()

    @database_sync_to_async
    def get_all_messages(self, chat_id):
        return Message.objects.order_by('-created_at').filter(chat_id=chat_id).all()[:30]

    @database_sync_to_async
    def get_receiver_profile_image(self):
        return ProfileImage.objects.get(user=self.receiver).path
