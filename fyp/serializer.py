from rest_framework import serializers
from .models import FYP, Participant
import datetime


class CreateFYPSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = FYP


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Participant


class GetAllFYPSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "user", "name", "description", "category", "technologies", "outcomes", "team_members",
                  "end_date", "participants", "days_left", "created_at", "updated_at"]
        model = FYP

    def get_participants(self, obj):
        participants_length = Participant.objects.filter(fyp=obj)
        return len(list(participants_length))

    def get_days_left(self, obj):
        print((obj.end_date - datetime.date.today()).days)
        return (obj.end_date - datetime.date.today()).days
