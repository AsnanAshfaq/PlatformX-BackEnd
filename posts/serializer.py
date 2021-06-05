from rest_framework import serializers
from .models import Comment, Post, Like, Share, Image, CommentVote, PostVote
from rest_framework.validators import UniqueValidator
from user.serializer import UserSerializer, ProfileImageSerializer, BackgroundImageSerializer
from user.models import User


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = "__all__"


class CommentUserSerializer(serializers.ModelSerializer):
    user_profile_image = ProfileImageSerializer()

    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'user_profile_image']


class CommentSerializer(serializers.ModelSerializer):
    votes = CommentVoteSerializer(many=True, read_only=True)
    user = CommentUserSerializer(required=False)

    class Meta:
        model = Comment
        exclude = ['post']


class LikeUserSerializer(serializers.ModelSerializer):
    # user_images = UserImageSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name']


class LikeSerializer(serializers.ModelSerializer):
    user = LikeUserSerializer()

    class Meta:
        model = Like
        exclude = ['post']


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        exclude = ["post"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = "__all__"


class PostUserSerializer(serializers.ModelSerializer):
    user_profile_image = ProfileImageSerializer()

    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'user_profile_image']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    votes = PostVoteSerializer(many=True)
    images = ImageSerializer(many=True)
    user = PostUserSerializer(required=False)

    class Meta:
        model = Post
        fields = ['id', 'votes', 'text', 'likes', 'images', 'comments', 'user']

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
