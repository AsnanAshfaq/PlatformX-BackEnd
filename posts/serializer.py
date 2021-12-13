from rest_framework import serializers
from .models import Post, Like, Image, PostVote, SavedPost
from user.serializer import UserSerializer, ProfileImageSerializer
from user.models import User
from .share.serializer import ShareSerializer
from .comment.serializer import CommentSerializer
from posts.like.serializer import LikeUserSerializer, LikeSerializer


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
    shares = ShareSerializer(many=True, required=False)
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
        return ""


class GetSavedPost(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = "__all__"


class GetSavedPosts(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    class Meta:
        model = SavedPost
        fields = ['post']

    def get_post(self, obj):
        query = self.context['query']
        return_post = []
        for post in query:
            post_query = Post.objects.filter(id=post['post_id'])
            serializer = PostSerializer(post_query, many=True, context=self.context)
            return_post.append(serializer.data[0])
        return return_post
