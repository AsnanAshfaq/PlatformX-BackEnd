from .views import get_comments, create_comment
from django.urls import path

urlpatterns = [
    path('<uuid:id>/comments/', get_comments),
    path('comment/create/', create_comment),
]
