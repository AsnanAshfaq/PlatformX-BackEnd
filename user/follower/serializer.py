from rest_framework import serializers
from user.models import Follower, User, ProfileImage


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    user_profile_image = ProfileImageSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "user_profile_image"]


class FollowerSerializer(serializers.ModelSerializer):
    followed_id = UserSerializer()

    class Meta:
        model = Follower
        exclude = ["follower_id"]


class FollowedSerializer(serializers.ModelSerializer):
    follower_id = UserSerializer()

    class Meta:
        model = Follower
        exclude = ["followed_id"]
