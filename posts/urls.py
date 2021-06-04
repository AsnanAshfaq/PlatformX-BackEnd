from django.urls import include, path
from rest_framework import routers
from .views import get_posts, create_post, CommentViewSet, ImagesViewSet
from rest_framework.authtoken import views

urlpatterns = [
    path('post/', get_posts),
    path('post/create/', create_post),
    path('post/comments/', CommentViewSet.as_view()),
    path('post/images/', ImagesViewSet.as_view())
]

# create   -- post
# read     -- get
# update   -- post
# delete   -- post
