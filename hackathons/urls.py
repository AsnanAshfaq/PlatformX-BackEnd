from django.urls import path, include
from .views import get_all_hackathons, get_hackathon

urlpatterns = [
    # path('post/', get_user_posts),
    path('hackathon/<uuid:id>/', get_hackathon),
    path('hackathons/', get_all_hackathons),
]
