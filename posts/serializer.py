from rest_framework import serializers
from .models import Comment, Post, Like, Share, Image, CommentVote, PostVote
from rest_framework.validators import UniqueValidator


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    votes = CommentVoteSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        exclude = ['post']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ["post"]


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


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    votes = PostVoteSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
