from jinja2.nodes import Pos
from rest_framework import serializers
from .models import User, Student, Organization, Follower, BackgroundImage, ProfileImage, Query
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
        exclude = ["password", "is_staff", "is_active", "is_superuser", "groups", "user_permissions"]

    def to_representation(self, instance):
        # ignore any field in User model which has null value
        result = super(UserSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class StudentProfileSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(required=False, source="user_profile_image")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "profile_image"]


class GetStudentSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(source='uuid')

    class Meta:
        model = Student
        fields = ["education", "bio", "lives_in", "skills", "interests", "date_of_birth", "phone_number", "linked_in",
                  "github", "twitter", "portfolio", "student"]


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

    def update(self, instance, validated_data):
        return instance


class EditStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.education = validated_data.get('education', instance.education)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.lives_in = validated_data.get('lives_in', instance.lives_in)
        instance.skills = validated_data.get('skills', instance.skills)
        instance.interests = validated_data.get('interests', instance.interests)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.linked_in = validated_data.get('linked_in', instance.linked_in)
        instance.github = validated_data.get('github', instance.github)
        instance.twitter = validated_data.get('twitter', instance.twitter)
        instance.portfolio = validated_data.get('portfolio', instance.portfolio)
        instance.save()
        return instance


class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = "__all__"

    def create(self, validated_data):
        return Query.objects.create(**validated_data)
