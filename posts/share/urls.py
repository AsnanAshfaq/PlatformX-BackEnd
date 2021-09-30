from django.urls import path
from .views import create_share, get_all_share

urlpatterns = [
    path('share/create/', create_share),
    path('shares/', get_all_share),

]
