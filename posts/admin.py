from django.contrib import admin
from posts.models import Post, Comment, Like, Image, CommentVote, Share, PostVote, SavedPost

# Register your models here.

admin.site.register([Post, Comment, Like, Image, CommentVote, Share, PostVote, SavedPost])
