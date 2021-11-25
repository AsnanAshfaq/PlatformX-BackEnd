from rest_framework import serializers
from .models import Participant, Internship
from user.models import Student, User, ProfileImage, Organization


class GetAllInternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = "__all__"
