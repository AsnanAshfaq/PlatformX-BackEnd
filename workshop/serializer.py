from rest_framework import serializers
from .models import Workshop, Participant, Speaker, PreRequisite
from user.models import Organization, ProfileImage, User, Student
# from django.utils.dates import
from datetime import datetime


# get all the workshops


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class UserOrganizationSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["profile_image"]


class OrganizationSerializer(serializers.ModelSerializer):
    user = UserOrganizationSerializer(source='uuid')

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'user']


class UserStudentSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["id", "first_name", "username", "last_name", "profile_image"]


class StudentSerializer(serializers.ModelSerializer):
    user = UserStudentSerializer(source='uuid')

    class Meta:
        model = Student
        fields = ['user']


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ["name", "email", "image", "about"]


class PreRequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreRequisite
        fields = ["title", "description"]


class CreateEditWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = "__all__"

    def create(self, validated_data):
        return Workshop.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class AllWorkshopSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(source='user')
    days_left = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = ['id', 'organization', 'topic', "charges", "is_paid", "status", 'description', "days_left", 'poster',
                  'created_at',
                  'updated_at']

    def get_days_left(self, obj):
        if (obj.event_date - datetime.now().date()).days > 0:
            return (obj.event_date - datetime.now().date()).days
        return 0

    def get_status(self, obj):
        if (obj.event_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"


class GetWorkshopSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(source='user')
    days_left = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    prerequisites = PreRequisiteSerializer(required=False, many=True, source='workshop_prerequisite')

    speaker = SpeakerSerializer(required=False)

    class Meta:
        model = Workshop
        fields = ['id', 'organization', 'topic', "charges", "is_paid", "status", 'description', "take_away",
                  "days_left", 'speaker', 'prerequisites', 'poster', "event_date", "start_time", "end_time",
                  'created_at',
                  'updated_at']

    def get_days_left(self, obj):
        if (obj.event_date - datetime.now().date()).days > 0:
            return (obj.event_date - datetime.now().date()).days
        return 0

    def get_status(self, obj):
        if (obj.event_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"


class GetWorkshopParticipantSerializer(serializers.ModelSerializer):
    student = StudentSerializer(source='id')

    class Meta:
        model = Participant
        fields = ['student']


class CreateParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"

    def create(self, validated_data):
        return Participant.objects.create(**validated_data)
