from rest_framework import serializers
from .models import User, Student, Organization, Follower, BackgroundImage, ProfileImage
from collections import OrderedDict


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class BackgroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundImage
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=False)
    organization = OrganizationSerializer(required=False)
    follower_id = FollowerSerializer(many=True)
    followed_id = FollowerSerializer(many=True)
    user_profile_image = ProfileImageSerializer(required=False)
    user_background_image = BackgroundImageSerializer(required=False)

    class Meta:
        model = User
        exclude = ["password", "date_joined", "is_staff", "is_active", "is_superuser", "groups", "user_permissions"]

    def to_representation(self, instance):
        # ignore any field in User model which has null value
        result = super(UserSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class Users(serializers.ModelSerializer):
    student = StudentSerializer(required=False)
    organization = OrganizationSerializer(required=False)
    follower_id = FollowerSerializer(many=True)
    followed_id = FollowerSerializer(many=True)
    user_profile_image = ProfileImageSerializer(required=False)
    user_background_image = BackgroundImageSerializer(required=False)

    class Meta:
        model = User
        exclude = ["password"]
