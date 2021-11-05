from rest_framework import serializers
from .models import Hackathon, Judge, Prize, Participant, JudgingCriteria
from user.serializer import UserSerializer
from user.models import User, Organization, ProfileImage, BackgroundImage, Follower, Student
from django.utils.timezone import now


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ["id", "metadata", "path"]


class UserFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


class HackathonUserSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["profile_image"]


class RegisterParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"


class ParticipantUserSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'profile_image']


class GetParticipantSerializer(serializers.ModelSerializer):
    user = ParticipantUserSerializer(source='id')

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


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    user = HackathonUserSerializer(source='uuid')

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'user']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"


class HackathonSerializer(serializers.ModelSerializer):
    judges = JudgeSerializer(many=True)
    prizes = PrizeSerializer(many=True)
    criteria = CriteriaSerializer(many=True)
    organization = OrganizationSerializer(required=False, source='user')
    participant = ParticipantSerializer(many=True)

    class Meta:
        model = Hackathon
        exclude = ["is_video_required", "upload_file_type", "is_public_voting_enable", "start_of_judging",
                   "end_of_judging", "result_announcement_date", "saved_type", "user"]


class HackathonBriefSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(required=False, source='user')
    total_prize = serializers.SerializerMethodField('calculate_prize')
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = ["id", "title", "tag_line", "description", "theme_tags", "start_of_hackathon",
                  "end_of_hackathon",
                  "prize_currency", "total_prize", "participants", "days_left", "organization",
                  "created_at",
                  "updated_at"]

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
        return (obj.end_of_hackathon - now()).days


class GetUserHackathonsSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(required=False, source='user')

    participants = serializers.SerializerMethodField()
    total_prize = serializers.SerializerMethodField('calculate_prize')
    days_left = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = ["id", "title", "tag_line", "days_left", "participants", "total_prize", "logo_image", "theme_tags",
                  "organization", "created_at",
                  "updated_at"]

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(hackathon=obj)
        return len(list(participants_length))

    def calculate_prize(self, obj):
        prizes = Prize.objects.filter(hackathon=obj).values('value')
        total_prize = 0
        for _, p in enumerate(prizes):
            total_prize += p['value']
        return total_prize

    def get_days_left(self, obj):
        return (obj.end_of_hackathon - now()).days


class CreateHackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        hackathon = Hackathon.objects.create(**validated_data)
        return hackathon

    def update(self, instance, validated_data):
        # instance.email = validated_data.get('email', instance.email)
        # instance.content = validated_data.get('content', instance.content)
        # instance.created = validated_data.get('created', instance.created)
        return instance
