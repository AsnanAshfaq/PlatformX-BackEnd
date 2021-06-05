from rest_framework import serializers
from .models import User, Student, Organization, Follower, BackgroundImage, ProfileImage


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
    user_profile_image = ProfileImageSerializer()
    user_background_image = BackgroundImageSerializer()

    class Meta:
        model = User
        fields = "__all__"
    # def validators(self, data):
    #     if (data['organization'] is None):
    #         print("Organization is none")
    #         self.Meta.exclude += 'organization'
    #     elif (data['student'] is None):
    #         self.Meta.exclude += 'student'
