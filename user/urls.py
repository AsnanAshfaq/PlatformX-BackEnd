from django.urls import include, path
from rest_framework import routers
from .views import get_user, get_all_users, create_follower, delete_follower
from rest_framework.authtoken import views

urlpatterns = [
    path('', get_user),
    path('all/', get_all_users),
    path('follower/create', create_follower),
    path('follower/delete', delete_follower)
]
