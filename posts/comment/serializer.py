from rest_framework import serializers
from posts.models import CommentVote
from user.serializer import ProfileImageSerializer
from user.models import User
from posts.models import Comment


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

