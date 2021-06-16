from django.urls import path, include
from .views import get_all_hackathons

urlpatterns = [
    # path('post/', get_user_posts),
    path('hackathons/', get_all_hackathons),
]
