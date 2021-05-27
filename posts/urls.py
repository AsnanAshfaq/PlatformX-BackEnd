from django.urls import include, path
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, ImagesViewSet
from rest_framework.authtoken import views

urlpatterns = [
    path('post/', PostViewSet.as_view()),
    path('post/comments/', CommentViewSet.as_view()),
    path('post/images/', ImagesViewSet.as_view())
]
