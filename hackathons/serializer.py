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


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = "__all__"


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
                  "submission_requirement", "background_image", "is_video_required", "start_date_of_hackathon",
                  "start_time_of_hackathon", "end_date_of_hackathon", "end_time_of_hackathon", "saved_type",
                  "prizes", "criteria", "participants", "days_left", "status", "is_applied", "created_at", "updated_at"]

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(hackathon=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        return (obj.end_date_of_hackathon - datetime.now().date()).days

    def get_status(self, obj):
        if (obj.end_date_of_hackathon - datetime.now().date()).days > 0:
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
        fields = ["id", "organization", "title", "tag_line", "theme_tags", "start_date_of_hackathon",
                  "background_image", "end_date_of_hackathon", "total_prize", "is_applied", "participants", "status",
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
        return (obj.end_date_of_hackathon - datetime.now().date()).days

    def get_status(self, obj):
        if (obj.end_date_of_hackathon - datetime.now().date()).days > 0:
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
                  "days_left", "status", "saved_type", "created_at", "updated_at"]

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
        if (obj.end_date_of_hackathon - datetime.now().date()).days > 0:
            return (obj.end_date_of_hackathon - datetime.now().date()).days
        return 0

    def get_status(self, obj):
        if (obj.end_date_of_hackathon - datetime.now().date()).days > 0:
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
        instance.contact_email = validated_data.get('contact_email', instance.contact_email)
        instance.is_team_required = validated_data.get('is_team_required', instance.is_team_required)
        instance.min_team_members = validated_data.get('min_team_members', instance.min_team_members)
        instance.max_team_members = validated_data.get('max_team_members', instance.max_team_members)
        instance.rules = validated_data.get('rules', instance.rules)
        instance.resource = validated_data.get('resource', instance.resource)
        instance.submission_requirement = validated_data.get('submission_requirement', instance.submission_requirement)

        # media fields
        instance.logo_image = validated_data.get('logo_image', instance.logo_image)
        instance.background_image = validated_data.get('background_image', instance.background_image)
        instance.allowed_file_types = validated_data.get('allowed_file_types', instance.allowed_file_types)
        instance.is_video_required = validated_data.get('is_video_required', instance.is_video_required)
        instance.promotional_video = validated_data.get('promotional_video', instance.promotional_video)

        # schedule fields
        instance.start_date_of_hackathon = validated_data.get('start_date_of_hackathon',
                                                              instance.start_date_of_hackathon)
        instance.start_time_of_hackathon = validated_data.get('start_time_of_hackathon',
                                                              instance.start_time_of_hackathon)
        instance.end_date_of_hackathon = validated_data.get('end_date_of_hackathon', instance.end_date_of_hackathon)
        instance.end_time_of_hackathon = validated_data.get('end_time_of_hackathon', instance.end_time_of_hackathon)
        instance.result_announcement_date = validated_data.get('result_announcement_date',
                                                               instance.result_announcement_date)
        instance.final_reminder = validated_data.get('final_reminder', instance.final_reminder)

        # saved type field
        instance.saved_type = validated_data.get('saved_type', instance.saved_type)

        instance.save()
        return instance
