from rest_framework.serializers import ModelSerializer
from user.models import BackgroundImage


class BackgroundImageSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = BackgroundImage

    def update(self, instance, validated_data):
        instance.path = validated_data.get('path', instance.path)
        instance.metadata = validated_data.get('metadata', instance.metadata)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
