from rest_framework import serializers
from .models import Workshop
from user.models import Organization, ProfileImage, User
# from django.utils.dates import
from datetime import datetime


# get all the workshops


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["profile_image"]


class OrganizationSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='uuid')

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'user']


class AllWorkshopSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(source='user')
    days_left = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = ['id', 'organization', 'topic', "charges", "is_paid", 'description', "days_left", 'poster',
                  'created_at',
                  'updated_at']

    def get_days_left(self, obj):
        return (obj.event_date - datetime.now().date()).days
