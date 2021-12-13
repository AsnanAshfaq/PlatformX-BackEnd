from rest_framework import serializers
from hackathons.models import Project, Evaluated, Result
from user.models import User, Student, ProfileImage


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ["id", "metadata", "path"]


class UserStudentSerializer(serializers.ModelSerializer):
    profile_image = UserProfileImageSerializer(source='user_profile_image')

    class Meta:
        model = User
        fields = ["id", "first_name", "username", 'email', "last_name", "profile_image"]


class StudentSerializer(serializers.ModelSerializer):
    user = UserStudentSerializer(source='uuid')

    class Meta:
        model = Student
        fields = ['user']


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


class GetProjectSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Project
        fields = ['id', 'student', 'title', 'description', 'tag_line', 'about', 'built_with', 'links', 'video_link',
                  'logo', 'file', 'created_at', 'updated_at']


class GetAllProjects(serializers.ModelSerializer):
    student = StudentSerializer()
    ratings = serializers.SerializerMethodField()
    marks = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'student', "ratings", "marks", 'title', 'tag_line', 'created_at', ]

    def get_ratings(self, obj):
        query = Evaluated.objects.filter(project=obj.id)
        if query.exists():
            query = Evaluated.objects.get(project=obj.id)
            return query.stars
        return 0

    def get_marks(self, obj):
        query = Evaluated.objects.filter(project=obj.id)
        total_marks = 0
        if query.exists():
            query = Evaluated.objects.get(project=obj.id)
            total_marks += query.idea
            total_marks += query.originality
            total_marks += query.functionality
            total_marks += query.design
            total_marks += query.problem
            return total_marks
        return 0


class CreateEditEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluated
        fields = "__all__"

    def create(self, validated_data):
        return Evaluated.objects.create(**validated_data)


class CreateEditResult(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"

    def create(self, validated_data):
        return Result.objects.create(**validated_data)


class GetResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"
