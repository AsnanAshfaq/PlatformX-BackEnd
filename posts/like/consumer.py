# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, SyncConsumer, AsyncWebsocketConsumer, \
    AsyncJsonWebsocketConsumer, AsyncConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
# from .models import Message, Chat
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer
from django.db.models import Q
from user.models import User
from posts.models import Like, Post
import json
from django.contrib.auth.models import AnonymousUser
from channels.exceptions import StopConsumer


class LikeConsumer(AsyncConsumer):

    async def websocket_connect(self, event):

        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.post_id = self.scope["url_route"]["kwargs"]["post_id"]

        # get user object using username
        user = await self.get_user_object(username=self.username)
        # get post object using post id
        post = await self.get_post_object(post=self.post_id)

        # call the like or dislike feature
        self.isLiked = await self.like_or_dislike(user=user, post=post)

        # get like count
        self.likeCount = await self.get_like_count(post=post)

        await self.channel_layer.group_add("post_like_channel", self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })

        print(f'[{self.username}] You are connected to the channel {self.channel_name}')

    async def websocket_receive(self, event):
        # print(f'[{self.user}] Recieved message {event["text"]}')
        #
        # # save it in the database
        # self.message = await self.save_message(user=self.user, message=event['text'])
        await self.channel_layer.group_send("post_like_channel", {
            "type": "send.message",
            "text": event["text"],
        })

    async def websocket_disconnect(self, close_code):

        await self.channel_layer.group_discard("post_like_channel", self.channel_name)

        await self.send({
            "type": "websocket.close",
            "code": close_code
        })

        print(f'[{self.username}] Disconnected with code {close_code}')

    async def send_message(self, event):
        print(f'[{self.username}] Post has been {self.isLiked}')
        # event['text'] = self.isLiked

        response = json.dumps({
            'isLiked': self.isLiked,
            'likeCount': str(self.likeCount)
        })
        await self.send({
            "type": "websocket.send",
            "text": response
        })

        await self.websocket_disconnect(4123)

    @database_sync_to_async
    def get_user_object(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            self.websocket_disconnect(4123)

    @database_sync_to_async
    def get_post_object(self, post):
        try:
            post = Post.objects.get(id=post)
            return post
        except Post.DoesNotExist:
            self.websocket_disconnect(4123)

    @database_sync_to_async
    def like_or_dislike(self, user, post):

        try:
            isLiked = Like.objects.filter(user=user, post=post)
            if isLiked:
                # it means user has liked the post, make it disliked
                isLiked.delete()
                return "DisLiked"
            else:
                # make the post liked by the user
                like = Like.objects.create(user=user, post=post)
                if like:
                    return "Liked"
        except Like.DoesNotExist:
            self.websocket_disconnect(4123)

    @database_sync_to_async
    def get_like_count(self, post):
        try:
            like = Like.objects.filter(post=post)
            return like.count()
        except Like.DoesNotExist:
            self.websocket_disconnect(4123)
