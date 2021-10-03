from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Message, Chat
from django.db.models import Q
from .serializer import GetMessagesSerializer, GetChatListMessageSerializer, UserSerializer
from user.models import User
import json


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, receiver):
    response = {}
    # get chat id
    sender_id = User.objects.get(email=request.user).id
    receiver_id = User.objects.get(username=receiver).id
    chat = Chat.objects.get(
        Q(user_first=sender_id, user_second=receiver_id) | Q(user_first=receiver_id, user_second=sender_id))
    messages = Message.objects.filter(chat_id=chat.id).order_by('-created_at')[:30]
    message_serializer = GetMessagesSerializer(messages, many=True)
    return Response(data=message_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_list(request):
    response = []
    try:
        user_id = User.objects.get(email=request.user).id
        # get chat id's where sender or receiver is current user
        chats = Chat.objects.filter(
            Q(user_first=user_id) | Q(user_second=user_id))
        print("User id is", user_id)
        for chat in chats:
            # get receiver id
            receiver = None
            if chat.user_first.id == user_id:
                receiver = chat.user_second
            elif chat.user_second.id == user_id:
                receiver = chat.user_first
            # getting receiver data
            receiver = User.objects.get(email=receiver)
            user_serializer = UserSerializer(receiver)

            # getting last message
            message_query = Message.objects.filter(chat_id=chat.id).order_by('-created_at')[0:1]
            message_serializer = GetChatListMessageSerializer(message_query, many=True)

            chat = {
                "id": chat.id,
                "user": user_serializer.data,
                "message": message_serializer.data[0]
            }
            response.append(chat)
        return Response(data=response, status=status.HTTP_200_OK)

    except:
        response['error'] = "Error occurred while fetching chats"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
