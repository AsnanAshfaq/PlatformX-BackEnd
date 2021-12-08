from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from workshop.models import Workshop, Participant, Speaker
from user.models import Organization, Student, User


class Mail:

    def __init__(self, workshop, ):
        self.workshop = workshop

    def send_mail_to_participant(self, user_mail):

        workshop_name = self.get_workshop_name()
        join_url = self.get_workshop_join_url()
        date = self.get_workshop_date()
        time = self.get_workshop_time()
        subject = "Workshop Invitation"
        message = f"Thanks for registering for {workshop_name}. Please set up zoom in your device.\n " \
                  f"Meeting join url is {join_url}. Join the meeting link on {date} at {time}\n"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_mail],
            # html_message=msg_html,
        )

    def send_mail_to_speaker(self):

        workshop_name = self.get_workshop_name()
        start_url = self.get_workshop_start_url()
        date = self.get_workshop_date()
        time = self.get_workshop_time()
        subject = "Workshop Invitation"
        message = f" Hey Speaker for {workshop_name}. We have schedule a zoom meeting for you\n " \
                  f"You can start the meeting by going to {start_url}\n" \
                  f"Join the meeting link on {date} at {time} \n" \
 \
            # get speaker mail
        speaker_mail = self.get_speaker_mail()
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[speaker_mail],
            # html_message=msg_html,
        )

    def send_mail_to_organization(self):

        # get participants list
        org_mail = self.get_org_mail()
        workshop_name = self.get_workshop_name()
        start_url = self.get_workshop_start_url()
        date = self.get_workshop_date()
        time = self.get_workshop_time()

        subject = "Workshop Invitation"
        message = f" Thank you for hosting workshop on PlatformX {workshop_name}.\n " \
                  f"We have schedule a zoom meeting for you.You can start the meeting by going to {start_url} \n " \
                  f"Join the meeting link on {date} at {time}"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[org_mail],
            fail_silently=False
            # html_message=msg_html,
        )

    def workshop_query(self):
        workshop_query = Workshop.objects.get(id=self.workshop.id)
        return workshop_query

    def get_attendees_mail(self):
        participant_query = Participant.objects.filter(workshop=self.workshop)
        attendees_mail_list = []
        for participant in participant_query:
            user = User.objects.get_by_natural_key(participant.id.uuid)
            attendees_mail_list.append(user.email)
        return attendees_mail_list

    def get_workshop_name(self):
        query = self.workshop_query()
        return query.topic

    def get_workshop_start_url(self):
        query = self.workshop_query()
        return query.start_url

    def get_workshop_date(self):
        query = self.workshop_query()
        return query.event_date

    def get_workshop_time(self):
        query = self.workshop_query()
        return query.start_time

    def get_org_mail(self):
        query = self.workshop_query()
        user = User.objects.get_by_natural_key(query.user.uuid)
        return user.email

    def get_speaker_mail(self):
        query = self.workshop_query()
        speaker_query = Speaker.objects.get(workshop=query.id)
        return speaker_query.email

    def get_workshop_join_url(self):
        query = self.workshop_query()
        return query.join_url
