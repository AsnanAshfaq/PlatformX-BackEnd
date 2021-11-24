from rest_framework import serializers
from .models import Test, Submission
from user.models import Student, ProfileImage, User
import requests


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "metadata", "path"]
        model = ProfileImage


class UserSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "profile_image"]


class StudentUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='uuid')

    class Meta:
        model = Student
        fields = ["uuid", "user"]


class CreateEditTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"

    def create(self, validated_data):
        return Test.objects.create(**validated_data)


class GetTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        exclude = ["fyp"]


class GetSubmissionSerializer(serializers.ModelSerializer):
    student = StudentUserSerializer(source='user')
    data = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ["id", "api_submission_id", "data", "fyp", "student", "created_at"]

    def get_data(self, obj):
        return 0
