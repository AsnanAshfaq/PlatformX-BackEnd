from rest_framework.serializers import ModelSerializer
from .models import Hackathon, Judge, Prize, Sponsor, Criteria
from user.serializer import UserSerializer
from user.models import User, Organization, ProfileImage, BackgroundImage, Follower


class CriteriaSerializer(ModelSerializer):
    class Meta:
        model = Criteria
        fields = "__all__"


class SponsorSerializer(ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class PrizeSerializer(ModelSerializer):
    class Meta:
        model = Prize
        fields = "__all__"


class JudgeSerializer(ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class UserProfileImageSerializer(ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class UserFollowersSerializer(ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


class HackathonUserSerializer(ModelSerializer):
    user_profile_image = UserProfileImageSerializer()

    class Meta:
        model = User
        exclude = ["password", "date_joined", "is_staff", "is_active", "is_superuser", "groups", "user_permissions"]


class OrganizationSerializer(ModelSerializer):
    organization = HackathonUserSerializer(source='uuid')

    class Meta:
        model = Organization
        fields = ['organization']


class HackathonSerializer(ModelSerializer):
    sponsors = SponsorSerializer(many=True, required=False)
    judges = JudgeSerializer(many=True)
    prizes = PrizeSerializer(many=True)
    criteria = CriteriaSerializer(many=True)
    user = OrganizationSerializer(required=False)

    class Meta:
        model = Hackathon
        fields = "__all__"
