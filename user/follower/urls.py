from django.urls import path
from .views import get_followers, get_following, create_follower, delete_follower

urlpatterns = [
    path('follower/', get_followers),
    path('following/', get_following),
    path('follower/create', create_follower),
    path('following/delete', delete_follower),
]
