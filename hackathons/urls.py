from django.urls import path, include
from .views import get_all_hackathons, get_hackathon, register, search_hackathon, get_user_hackathons

urlpatterns = [
    path('hackathon/<uuid:id>/register/', register),
    path('hackathon/<uuid:id>/', get_hackathon),
    path('hackathon/search/', search_hackathon),
    path('hackathon/', get_user_hackathons),
    path('hackathons/', get_all_hackathons),
    path('hackathon/share/', include('hackathons.share.urls')),
]
