from rest_framework import serializers
from .models import User, Student, Organization, Follower


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


class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    follower_id = FollowerSerializer(read_only=True, many=True)
    followed_id = FollowerSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = "__all__"
