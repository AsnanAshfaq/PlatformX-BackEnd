from django.urls import include, path
from rest_framework import routers
from .views import get_user, get_all_users
from rest_framework.authtoken import views
from .follower.views import get_followers, get_following, create_follower, delete_follower

urlpatterns = [
    path('', get_user),
    path('all/', get_all_users),
    path('follower/', get_followers),
    path('following/', get_following),
    path('follower/create', create_follower),
    path('following/delete', delete_follower)
]
