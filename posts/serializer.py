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
    votes = CommentVoteSerializer(many=True, required=False)
    user = CommentUserSerializer(required=False)

    class Meta:
        model = Comment
        # exclude = ['post']
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        validated_data['text'] = self.data['text']
        comment = Comment.objects.create(**validated_data)
        return comment


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

    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
        return image

    def update(self, instance, validated_data):
        instance.path = validated_data.get('path', instance.path)
        instance.metadata = validated_data.get('metadata', instance.metadata)
        instance.save()
        return instance


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
    comments = CommentSerializer(many=True, required=False)  # required=False
    likes = LikeSerializer(many=True, required=False)  # required=False
    votes = PostVoteSerializer(many=True, required=False)  # required=False
    images = ImageSerializer(many=True, required=False)  # required=False
    user = PostUserSerializer(required=False)  # required=False
    is_editable = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

    def get_is_editable(self, obj):
        # if the user logged in has made this post then enable the editing option
        user = UserSerializer(self.context['request'].user)

        if str(obj.user.id) == str(user.data['id']):
            return True
        return False

    def get_isLiked(self, obj):
        user = UserSerializer(self.context['request'].user)

        # query in like model where corresponding post and current user is found
        like_query = Like.objects.filter(post=obj, user=user.data['id'])

        if like_query:
            return "Liked"
        return "DisLiked"
