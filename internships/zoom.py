from .models import Internship
from rest_framework.response import Response
from rest_framework import status
import requests
from user.models import Organization, User
import random, string


class ZoomAPI:
    token = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6ImNMVGJRSXJFUzdxQjNVRENkSl9KM3ciLCJleHAiOjE2Njg4NjM3NjAsImlhdCI6MTYzNzMyMjM4OH0.M-Cx75XFz3tBdBw4vzqvt5jF1E3KgnTQNZZdC_GWBgg'
    base_url = "https://api.zoom.us/v2/"

    headers = {
        "Authorization": token
    }
    body = {
        "type": 2,  # schedule
        "settings": {
            "host_video": True,
            "participant_video": False,
            "cn_meeting": False,
            "in_meeting": False,
            "join_before_host": False,
            "mute_upon_entry": True,
            "watermark": False,
            "use_pmi": False,
            "approval_type": 1,  # manual approval of registrants
            "registration_type": 1,  # attendees register once and can attend any meeting occurrence
            "audio": "both",  # telephony and voip
            "auto_recording": "none",
            "alternative_hosts": "",  # add email address of the manager of the meeting
            "close_registration": True,  # close registration after event date
            "waiting_room": True,  # enable waiting room
            "registrants_email_notification": True,
            "registrants_confirmation_email": True,  # sends registrants an email confirmation
            "meeting_authentication": False,
            "authentication_option": "",
            "authentication_domains": "",
            "alternative_hosts_email_notification": ""  # add email address of the manager of the workshop
        },
    }

    def __init__(self, internship, std_id, time):
        self.id = internship
        self.std_id = std_id
        self.time = time
        self.response = None

    def create_meeting(self):
        self.body['topic'] = self.get_internship_name()
        self.body['agenda'] = self.get_internship_description()
        self.body['password'] = self.generate_password()
        self.body["start_time"] = self.time
        self.body['timezone'] = "Asia/Tashkent"
        self.body['schedule_for'] = self.get_organization_email()
        self.body['contact_email'] = self.get_organization_email()
        # self.body['settings']['alternative_hosts'] = self.get_organization_email()
        self.body['settings']['contact_name'] = self.get_organization_name()

        response = requests.post(self.base_url + "users/me/meetings", json=self.body, headers=self.headers)
        if response.status_code == 201:
            self.response = response.json()
            return 1
        return 0

    def get_internship_name(self):
        query = self.internship_query()
        return query.name

    def get_workshop_start_time(self):
        query = self.internship_query()
        return query.event_date.strftime('%Y/%m/%d') + "T" + query.start_time.strftime('%H/%M/%S') + "Z"

    def get_organization_email(self):
        query = self.internship_query()
        user = User.objects.get_by_natural_key(query.user.uuid)
        return user.email

    def get_organization_name(self):
        query = self.internship_query()
        user = Organization.objects.get(uuid=query.user.uuid)
        return user.name

    def get_internship_description(self):
        query = self.internship_query()
        return query.description

    def set_response(self, json):
        self.response = json

    def get_response(self):
        return self.response

    def internship_query(self):
        internship = Internship.objects.get(id=self.id)
        if internship:
            return internship
        else:
            self.reject_request()

    def generate_password(self):
        return "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))

    def reject_request(self):
        return 0
