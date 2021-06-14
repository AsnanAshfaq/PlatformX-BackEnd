from django.urls import include, path
from rest_framework import routers
from .views import get_all_posts, create_post, ImagesViewSet, create_comment, get_comments, get_user_posts
from rest_framework.authtoken import views

urlpatterns = [
    path('post/<uuid:id>/comment/', get_comments),
    path('post/comment/create', create_comment),
    path('post/create/', create_post),
    path('post/', get_user_posts),
    path('posts/', get_all_posts),
]
