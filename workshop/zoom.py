from workshop.models import Workshop
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
        "type": 1,  # for now
        # "start_time": "2020-06-26T14:30:00Z",
        # "duration": 60,
        # "recurrence": {
        #     "type": "1",
        #     "repeat_interval": "1",
        #     "weekly_days": "4",
        #     "monthly_day": 30,
        #     "monthly_week": "4",
        #     "monthly_week_day": "4",
        #     "end_times": 1,
        #     "end_date_time": "2020-07-04T16:20:00Z"
        # },
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
            "contact_name": "Asnan",  # contact name for meeting registration
            "contact_email": "18asnan@gmail.com",  # contact email address for meeting registration
            "registrants_email_notification": True,
            "registrants_confirmation_email": True,  # sends registrants an email confirmation
            "meeting_authentication": False,
            "authentication_option": "",
            "authentication_domains": "",
            "alternative_hosts_email_notification": ""  # add email address of the manager of the workshop
        },
    }

    def __init__(self, workshop):
        self.workshop = workshop

    def create_meeting(self):
        self.body['topic'] = self.get_workshop_name()
        self.body['password'] = self.generate_password()
        self.body["start_time"] = self.get_workshop_start_time()
        self.body['schedule_for'] = self.get_organization_email()
        self.body['agenda'] = self.get_workshop_description()
        response = requests.post(self.base_url + "users/me/meetings", json=self.body, headers=self.headers)
        if response.status_code == 201:
            self.set_response(json=response.json)
            return 1
        return 0

    def get_workshop_name(self):
        query = self.workshop_query()
        return query.topic

    def get_workshop_start_time(self):
        query = self.workshop_query()
        return query.event_date.strftime('%Y/%m/%d') + "T" + query.start_time.strftime('%H/%M/%S') + "Z"

    def get_organization_email(self):
        workshop_query = self.workshop_query()
        user = User.objects.get_by_natural_key(workshop_query.user.uuid)
        return "18asnan@gmail.com"

    def get_workshop_description(self):
        query = self.workshop_query()
        return query.description

    def set_response(self, json):
        self.response = json

    def get_response(self):
        return self.response

    def workshop_query(self):
        workshop_query = Workshop.objects.get(id=self.workshop)
        if workshop_query:
            return workshop_query
        else:
            self.reject_request()

    def generate_password(self):
        return "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))

    def reject_request(self):
        return 0
