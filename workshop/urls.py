from django.urls import include, path
from .views import get_workshops

urlpatterns = [
    path('workshops/', get_workshops),
    path('workshop/share/', include('workshop.share.urls')),
]