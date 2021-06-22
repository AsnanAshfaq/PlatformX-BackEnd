from rest_framework import serializers
from .models import Hackathon, Judge, Prize, Sponsor, Criteria
from user.serializer import UserSerializer
from user.models import User, Organization, ProfileImage, BackgroundImage, Follower


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = "__all__"


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = "__all__"


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class UserFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


class HackathonUserSerializer(serializers.ModelSerializer):
    user_profile_image = UserProfileImageSerializer()

    class Meta:
        model = User
        fields = ["user_profile_image"]


class OrganizationSerializer(serializers.ModelSerializer):
    user = HackathonUserSerializer(source='uuid')

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'user']


class HackathonSerializer(serializers.ModelSerializer):
    sponsors = SponsorSerializer(many=True, required=False)
    judges = JudgeSerializer(many=True)
    prizes = PrizeSerializer(many=True)
    criteria = CriteriaSerializer(many=True)
    organization = OrganizationSerializer(required=False, source='user')

    class Meta:
        model = Hackathon
        exclude = ["is_video_required", "upload_file_type", "is_public_voting_enable", "start_of_judging",
                   "end_of_judging", "result_announcement_date", "saved_type", "user"]


class HackathonBriefSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(required=False, source='user')
    total_prize = serializers.SerializerMethodField('calculate_prize')

    class Meta:
        model = Hackathon
        fields = ["id", "title", "tag_line", "description", "theme_tags", "start_of_hackathon", "end_of_hackathon",
                  "prize_currency", "total_prize", "thumbnail_image", "organization", "created_at", "updated_at"]

    def calculate_prize(self, obj):
        prizes = Prize.objects.filter(hackathon=obj).values('value')
        total_prize = 0
        for _, p in enumerate(prizes):
            total_prize += p['value']
        return total_prize
