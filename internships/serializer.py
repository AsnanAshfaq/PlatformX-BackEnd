from rest_framework import serializers
from .models import Participant, Internship
from user.models import Student, User, ProfileImage, Organization
from datetime import datetime


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "metadata", "path"]
        model = ProfileImage


class UserSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "profile_image"]


class OrganizationSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='uuid')

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'user']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='uuid')

    class Meta:
        model = Student
        fields = ['uuid', 'user']


class GetAllInternshipSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    organization = OrganizationSerializer(source='user')
    is_applied = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = ["id", "name", "organization", "description", "duration",
                  "is_paid", "days_left", "end_date", "status", "stipend", "is_applied", "created_at", "updated_at"]

    def get_status(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"

    def get_days_left(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return (obj.end_date - datetime.now().date()).days
        return 0

    def get_is_applied(self, obj):
        user = UserSerializer(self.context['request'].user)
        if Participant.objects.filter(internship=obj.id, id=user.data['id']).exists():
            return True
        return False


class GetInternshipSerializer(serializers.ModelSerializer):
    days_left = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    organization = OrganizationSerializer(source='user')
    status = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = ["id", "name", "organization", "description", "skills", "responsibilities", "duration",
                  "is_paid", "end_date", "stipend", "days_left", "is_applied", "status", "created_at", "updated_at"]

    def get_status(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"

    def get_days_left(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return (obj.end_date - datetime.now().date()).days
        return 0

    def get_is_applied(self, obj):
        user = UserSerializer(self.context['request'].user)
        if Participant.objects.filter(internship=obj.id, id=user.data['id']).exists():
            return True
        return False


class CreateEditInternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = "__all__"

    def create(self, validated_data):
        return Internship.objects.create(**validated_data)


class CreateParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"

    def create(self, validated_data):
        return Participant.objects.create(**validated_data)


class GetInternshipParticipantsSerializer(serializers.ModelSerializer):
    student = StudentSerializer(source='id')

    class Meta:
        model = Participant
        fields = ["student", "github", 'linked_in', 'portfolio', 'cv', 'resume', 'created_at', 'updated_at']


class GetOrganizationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = ["id", "name", "description", "skills", "responsibilities", "duration",
                  "is_paid", "end_date", "stipend", "days_left", "participants", "status", "created_at", "updated_at"]

    def get_status(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"

    def get_days_left(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return (obj.end_date - datetime.now().date()).days
        return 0

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(internship=obj)
        return len(list(participants_length))
