from rest_framework import serializers
from posts.models import Share, Post
from user.models import ProfileImage, User
from posts.models import Image


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = "__all__"


# all the serializers below are for get_all_share() view
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class PostUserSerializer(serializers.ModelSerializer):
    user_profile_image = ProfileImageSerializer()

    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'user_profile_image']


class PostSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(required=False)  # required=False
    images = ImageSerializer(many=True, required=False)  # required=False

    class Meta:
        model = Post
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    user_profile_image = ProfileImageSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "user_profile_image"]


class GetAllSharesSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    user = UserSerializer()

    class Meta:
        model = Share
        fields = "__all__"
