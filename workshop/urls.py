from django.urls import include, path
from .views import get_workshops, search_workshop

urlpatterns = [
    path('workshops/', get_workshops),
    path('workshop/search/', search_workshop),
    path('workshop/share/', include('workshop.share.urls')),
]
