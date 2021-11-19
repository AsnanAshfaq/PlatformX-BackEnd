from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from workshop.models import Workshop, Participant
from user.models import Organization, Student, User


class Mail:

    def __init__(self, workshop, data):
        self.workshop = workshop
        self.data = data()

    def send_mail_to_attendees(self):
        msg_html = render_to_string('workshop_join_invitation_mail.html',
                                    {'topic': self.data['topic'], 'agenda': self.data['agenda'],
                                     'join_url': self.data['join_url'], 'password': self.data['password'],
                                     'contact_email': self.data['settings']['contact_email']})

        # get participants list
        attendees_mail = self.get_attendees_mail()
        send_mail(
            subject="Workshop invitation",
            message="Workshop invitation",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=attendees_mail,
            html_message=msg_html,
        )

    def workshop_query(self):
        workshop_query = Workshop.objects.get(id=self.workshop)
        return workshop_query

    def get_attendees_mail(self):
        participant_query = Participant.objects.filter(workshop=self.workshop)
        attendees_mail_list = []
        for participant in participant_query:
            user = User.objects.get_by_natural_key(participant.id.uuid)
            attendees_mail_list.append(user.email)
        return attendees_mail_list

    def workshop_organizer_invitation_mail(self):
        pass
