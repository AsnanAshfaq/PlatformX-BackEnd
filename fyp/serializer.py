from rest_framework import serializers
from .models import FYP, Participant
import datetime
from user.models import Organization, ProfileImage, User


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "metadata", "path"]
        model = ProfileImage


class UserSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["profile_image"]


class OrganizationSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='uuid')

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'user']


class CreateFYPSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = FYP


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Participant


class CreateFYPSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = FYP

    def create(self, validated_data):
        return FYP.objects.create(**validated_data)


class CreateParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"

    def create(self, validated_data):
        return Participant.objects.create(**validated_data)


class GetAllFYPSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    organization = OrganizationSerializer(source='user')

    class Meta:
        fields = ["id", "organization", "name", "description", "category", "technologies", "outcomes", "team_members",
                  "end_date", "participants", "days_left", "created_at", "updated_at"]
        model = FYP

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(fyp=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        return (obj.end_date - datetime.date.today()).days


class GetFYPSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    organization = OrganizationSerializer(source='user')

    class Meta:
        fields = ["id", "organization", "name", "description", "category", "technologies", "outcomes", "team_members",
                  "end_date", "participants", "days_left", "created_at", "updated_at"]
        model = FYP

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(fyp=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        return (obj.end_date - datetime.date.today()).days


class GetOrganizationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "name", "description", "category", "technologies", "outcomes", "team_members",
                  "end_date", "participants", "days_left", "created_at", "updated_at"]
        model = FYP

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(fyp=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        return (obj.end_date - datetime.date.today()).days
