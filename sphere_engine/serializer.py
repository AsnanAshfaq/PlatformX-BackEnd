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


class GetAllSubmissionSerializer(serializers.ModelSerializer):
    student = StudentUserSerializer(source='user')
    data = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ["id", "api_submission_id", "data", "student", "created_at"]

    def get_data(self, obj):
        data = {}
        url = f'https://8d2123f3.compilers.sphere-engine.com/api/v4/submissions/{obj.api_submission_id}?access_token=dc64519a0564fd943e20b09564ac9be5'
        response = requests.get(url)
        j = response.json()
        data['executing'] = j['executing']
        data['result'] = j['result']
        return data


class GetSubmissionSerializer(serializers.ModelSerializer):
    student = StudentUserSerializer(source='user')
    data = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ["id", "api_submission_id", "data", "student", "created_at"]

    def get_data(self, obj):
        url = f'https://8d2123f3.compilers.sphere-engine.com/api/v4/submissions/{obj.api_submission_id}?access_token=dc64519a0564fd943e20b09564ac9be5'
        response = requests.get(url)
        j = response.json()
        return j
