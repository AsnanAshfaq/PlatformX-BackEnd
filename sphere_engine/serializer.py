from rest_framework import serializers
from .models import Test, Submission
from user.models import Student, ProfileImage, User
import requests

sphere_engine_token = "4d1ee35c10df434a08061219c07e4d9a"


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
        url = f'https://8d2123f3.compilers.sphere-engine.com/api/v4/submissions/{obj.api_submission_id}?access_token={sphere_engine_token}'
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
        url = f'https://8d2123f3.compilers.sphere-engine.com/api/v4/submissions/{obj.api_submission_id}?access_token={sphere_engine_token}'
        response = requests.get(url)
        j = response.json()
        return j


class GetStudentSubmissionSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ["fyp", "api_submission_id", "data"]

    def get_data(self, obj):
        url = f'https://8d2123f3.compilers.sphere-engine.com/api/v4/submissions/{obj.api_submission_id}?access_token={sphere_engine_token}'
        response = requests.get(url)
        j = response.json()
        return j


class CreateSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"

    def create(self, validated_data):
        return Submission.objects.create(**validated_data)
