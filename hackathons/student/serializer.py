from rest_framework import serializers
from hackathons.models import Participant, Hackathon
from user.serializer import UserSerializer
from user.models import User, Organization, ProfileImage, BackgroundImage, Follower, Student
from django.utils.timezone import now
from datetime import datetime


class RegisterParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"

    def create(self, validated_data):
        return Participant.objects.create(**validated_data)
