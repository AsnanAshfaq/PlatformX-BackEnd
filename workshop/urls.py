from django.urls import include, path
from .views import get_workshops, search_workshop, get_workshop, create_workshop, start_workshop

urlpatterns = [
    path('workshop/<uuid:id>/', get_workshop),
    path('workshop/create/', create_workshop),
    path('workshop/start/', start_workshop),
    path('workshops/', get_workshops),
    path('workshop/search/', search_workshop),
    path('workshop/share/', include('workshop.share.urls')),
]
