from rest_framework import serializers
from .models import Message, Chat
from user.models import User, ProfileImage


class AuthorProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ['path']


class AuthorSerializer(serializers.ModelSerializer):
    profile_image = AuthorProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_image']


class GetMessagesSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Message
        fields = ['id', 'author', 'message', 'created_at']


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'profile_image']


class GetChatListMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'message', 'created_at', 'updated_at', 'author']
