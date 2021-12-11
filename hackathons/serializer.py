from rest_framework import serializers
from .models import Hackathon, Prize, Participant, JudgingCriteria
from user.serializer import UserSerializer
from user.models import User, Organization, ProfileImage, BackgroundImage, Follower, Student
from django.utils.timezone import now
from datetime import datetime


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ["id", "metadata", "path"]


class UserStudentSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["id", "first_name", "username", "last_name", "profile_image"]


class UserFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


class HackathonUserSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["profile_image"]


class ParticipantUserSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', "profile_image"]


class GetParticipantSerializer(serializers.ModelSerializer):
    user = ParticipantUserSerializer()

    class Meta:
        model = Participant
        fields = ["user"]


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgingCriteria
        fields = "__all__"

    def create(self, validated_data):
        return JudgingCriteria.objects.create(**validated_data)


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = "__all__"

    def create(self, validated_data):
        return Prize.objects.create(**validated_data)


class OrganizationSerializer(serializers.ModelSerializer):
    user = HackathonUserSerializer(source='uuid')

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'user']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"


class GetHackathonSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(required=False, source='user')
    prizes = PrizeSerializer(many=True)
    criteria = CriteriaSerializer(many=True, source='hackathon_judging_criteria')
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = ["id", "organization", "title", "tag_line", "description", "theme_tags", "rules", "resource",
                  "submission_requirement", "background_image", "event_date", "prizes", "criteria",
                  "participants", "days_left", "status", "is_applied", "created_at", "updated_at"]

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(hackathon=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        return (obj.event_date - datetime.now().date()).days

    def get_status(self, obj):
        if (obj.event_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"

    def get_is_applied(self, obj):
        user = UserStudentSerializer(self.context['request'].user)
        if Participant.objects.filter(hackathon=obj.id, user=user.data['id']).exists():
            return True
        return False


class AllHackathonSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(required=False, source='user')
    total_prize = serializers.SerializerMethodField('calculate_prize')
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = ["id", "organization", "title", "tag_line", "theme_tags",
                  "background_image", "event_date", "total_prize", "is_applied", "participants", "status",
                  "days_left", "created_at", "updated_at"]

    def calculate_prize(self, obj):
        prizes = Prize.objects.filter(hackathon=obj).values('value')
        total_prize = 0
        for _, p in enumerate(prizes):
            total_prize += p['value']
        return total_prize

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(hackathon=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        return (obj.event_date - datetime.now().date()).days

    def get_status(self, obj):
        if (obj.event_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"

    def get_is_applied(self, obj):
        user = UserStudentSerializer(self.context['request'].user)
        if Participant.objects.filter(hackathon=obj.id, user=user.data['id']).exists():
            return True
        return False


class GetUserHackathonsSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    total_prize = serializers.SerializerMethodField('calculate_prize')
    days_left = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = ["id", "title", "tag_line", "theme_tags", "background_image", "total_prize", "participants",
                  "days_left", "status", "created_at", "updated_at"]

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(hackathon=obj)
        if len(list(participants_length)) > 0:
            return len(list(participants_length))
        return 0

    def calculate_prize(self, obj):
        prizes = Prize.objects.filter(hackathon=obj).values('value')
        total_prize = 0
        for _, p in enumerate(prizes):
            total_prize += p['value']
        return total_prize

    def get_days_left(self, obj):
        if (obj.event_date - datetime.now().date()).days > 0:
            return (obj.event_date - datetime.now().date()).days
        return 0

    def get_status(self, obj):
        if (obj.event_date - datetime.now().date()).days > 0:
            return "Open"
        return "Ended"


class CreateEditHackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        hackathon = Hackathon.objects.create(**validated_data)
        return hackathon

    def update(self, instance, validated_data):
        # general fields
        instance.title = validated_data.get('title', instance.title)
        instance.tag_line = validated_data.get('tag_line', instance.tag_line)
        instance.description = validated_data.get('description', instance.description)
        instance.theme_tags = validated_data.get('theme_tags', instance.theme_tags)
        instance.rules = validated_data.get('rules', instance.rules)
        instance.resource = validated_data.get('resource', instance.resource)
        instance.submission_requirement = validated_data.get('submission_requirement', instance.submission_requirement)

        # media fields
        instance.logo_image = validated_data.get('logo_image', instance.logo_image)
        instance.background_image = validated_data.get('background_image', instance.background_image)

        # schedule fields
        instance.event_date = validated_data.get('event_date', instance.event_date)

        instance.save()
        return instance
