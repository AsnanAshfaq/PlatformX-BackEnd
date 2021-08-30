from django.urls import include, path
from rest_framework import routers
from .views import get_user, get_all_users, create_user, signin, activate_user, password_reset, verify_code
from rest_framework.authtoken import views
from .follower.views import get_followers, get_following, create_follower, delete_follower

urlpatterns = [
    path('', get_user),
    path('signup/', create_user),
    path('signin/', signin),
    path('password_reset/', password_reset),
    path('verify_code/', verify_code),
    path('all/', get_all_users),
    path('activate/', activate_user),
    path('follower/', get_followers),
    path('following/', get_following),
    path('follower/create', create_follower),
    path('following/delete', delete_follower)
]
