from django.db import models
import uuid


# Create your models here.


class Post(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE,related_name="post", default=1)
    text = models.TextField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class PostVote(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    value = models.IntegerField(null=False)
    status = models.CharField(max_length=10)


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, related_name="user", default=1)
    text = models.TextField(max_length=500, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", null=False)

    def __str__(self):
        return str(self.id)


class CommentVote(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="votes")
    value = models.IntegerField(null=False)
    status = models.CharField(max_length=10)


class Like(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, default=1)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes", null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Share(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        'user.User', on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="shares", null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Image(models.Model):

    def get_image_path_and_filename(self, filename):
        return "post_images" + "/" + str(self.post) + "/" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images", null=False)
    metadata = models.CharField(max_length=30, default="", null=True, blank=True)
    path = models.ImageField(upload_to=get_image_path_and_filename, default="", )

    def __str__(self):
        return str(self.id) + self.metadata
