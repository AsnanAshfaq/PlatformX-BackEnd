from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from google.cloud import storage
# from firebase_admin import messaging
import os
from datetime import datetime


def push_notification(user):
    # function to send notification to user

    print(list(FCMDevice.objects.all().values('registration_id')))

    message = Message(
        data={
            "Nick": "Mario",
            "body": "great match!",
            "Room": "PortugalVSDenmark"
        },
        topic="Testing",
        token="AAAAyD2GWsE:APA91bGiv6LOWRASZE6VLTzG2bwQ4msovJF-ul5M8wCb3gw6rQoxtOGxPeJAwiQgeQtHQtMeEd1bWMuJ-Gu1q_1kuJ2MI1tfCvJxr9RCJEPHK-0k-cz2Q4pvO9exk-Z0lh3T_tQhMiyA",
    )
    FCMDevice.objects.send_message(message=message)
