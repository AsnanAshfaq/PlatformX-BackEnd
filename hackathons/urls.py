from django.urls import path, include
from .views import get_all_hackathons, get_hackathon, search_hackathon, get_participants, \
    search_participants

from .organization.views import create_hackathon, edit_hackathon, get_organization_hackathons
from .student.views import register

urlpatterns = [
    path('hackathon/<uuid:id>/register/', register),
    path('hackathon/<uuid:id>/project/', include('hackathons.project.urls')),
    path('hackathon/<uuid:id>/participants/', get_participants),
    path('hackathon/<uuid:id>/participants/search/', search_participants),
    path('hackathon/<uuid:id>/', get_hackathon),
    path('hackathon/search/', search_hackathon),
    path('hackathon/create/', create_hackathon),
    path('hackathon/edit/', edit_hackathon),
    path('hackathon/', get_organization_hackathons),
    path('hackathons/', get_all_hackathons),
    path('hackathon/share/', include('hackathons.share.urls')),
]
