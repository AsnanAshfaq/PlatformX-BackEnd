from rest_framework import serializers
from .models import FYP, Participant
from datetime import datetime
from user.models import Organization, ProfileImage, User


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "metadata", "path"]
        model = ProfileImage


class UserSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["id", "profile_image"]


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


class CreateEditParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"

    def create(self, validated_data):
        return Participant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print("Updating participant")
        instance.user = validated_data.get('user', instance.user)
        instance.fyp = validated_data.get('fyp', instance.fyp)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.is_meeting_scheduled = validated_data.get('is_meeting_scheduled', instance.is_meeting_scheduled)
        instance.meeting_schedule = validated_data.get('meeting_schedule', instance.meeting_schedule)
        instance.meeting_id = validated_data.get('meeting_id', instance.meeting_id)
        return instance


class GetAllFYPSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    organization = OrganizationSerializer(source='user')
    is_applied = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "organization", "name", "description", "category", "technologies", "outcomes",
                  "team_members", "end_date", "participants", "days_left", "is_applied", "status", "created_at",
                  "updated_at"]
        model = FYP

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(fyp=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return (obj.end_date - datetime.now().date()).days
        return 0

    def get_is_applied(self, obj):
        user = UserSerializer(self.context['request'].user)
        if Participant.objects.filter(fyp=obj.id, user=user.data['id']).exists():
            return True
        return False

    def get_status(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"


class GetFYPSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    organization = OrganizationSerializer(source='user')
    is_applied = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "organization", "name", "description", "category", "technologies", "outcomes", "team_members",
                  "end_date", "participants", "is_applied", "days_left", "status", "created_at", "updated_at"]
        model = FYP

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(fyp=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return (obj.end_date - datetime.now().date()).days
        return 0

    def get_is_applied(self, obj):
        user = UserSerializer(self.context['request'].user)
        if Participant.objects.filter(fyp=obj.id, user=user.data['id']).exists():
            return True
        return False

    def get_status(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"


class GetOrganizationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "name", "description", "category", "technologies", "outcomes", "team_members",
                  "end_date", "participants", "days_left", "status", "created_at", "updated_at"]
        model = FYP

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(fyp=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return (obj.end_date - datetime.now().date()).days
        return 0

    def get_status(self, obj):
        if (obj.end_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"
