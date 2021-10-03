from django.urls import path, include
from .views import get_messages, get_chat_list

urlpatterns = [
    path('messages/<str:receiver>/', get_messages),
    path('list/', get_chat_list)
]
