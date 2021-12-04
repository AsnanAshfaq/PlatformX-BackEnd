from rest_framework import serializers
from hackathons.models import Project


class CreateEditProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.tag_line = validated_data.get('tag_line', instance.tag_line)
        instance.about = validated_data.get('about', instance.about)
        instance.built_with = validated_data.get('built_with', instance.built_with)
        instance.links = validated_data.get('links', instance.links)
        instance.video_link = validated_data.get('video_link', instance.video_link)
        instance.save()
        return instance
