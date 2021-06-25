from django.urls import path, include
from .views import get_all_hackathons, get_hackathon, register

urlpatterns = [
    path('hackathon/<uuid:id>/register/', register),
    # path('post/', get_user_posts),
    # path('hackathon/<uuid:id>/participants', get_participants),
    path('hackathon/<uuid:id>/', get_hackathon),
    path('hackathons/', get_all_hackathons),
]
