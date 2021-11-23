from rest_framework import serializers
from .models import Test, Submission


class CreateEditTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"

    def create(self, validated_data):
        return Test.objects.create(**validated_data)


class GetTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        exclude = ["fyp"]
