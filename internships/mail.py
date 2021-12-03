from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .models import Internship, Participant
from user.models import Organization, Student, User


class Mail:

    def __init__(self, internship_id, applicant_id, data):
        self.internship_id = internship_id
        self.applicant_id = applicant_id
        self.data = data()

    def send_mail_to_applicant(self):
        # msg_html = render_to_string('internship_applicant_interview_mail.html')

        # get applicant list
        # applicant_mail = self.get_applicant_mail()
        message = "My message"
        subject = "Password Reset"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["18asnan@gmail.com"],
            fail_silently=False
            # html_message=msg_html,
        )

    def send_mail_to_organization(self):
        msg_html = render_to_string('internship_applicant_interview_mail.html')

        # get applicant list
        applicant_mail = self.get_applicant_mail()
        send_mail(
            subject="Internship Interview",
            message="Here is the message",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["18asnan@gmail.com"],
            fail_silently=False
            # html_message=msg_html,
        )

    def get_applicant_mail(self):
        user = User.objects.get(id=self.applicant_id)
        return user.email
