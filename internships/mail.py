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

    def send_mail_to_applicant(self, join_url, join_time):
        # msg_html = render_to_string('internship_applicant_interview_mail.html')

        # get applicant list
        applicant_mail = self.get_applicant_mail()
        internship_name = self.get_internship_name()
        subject = "Internship Interview"
        message = f" Congratulations! You have been shortlisted for an online interview for {internship_name}.\n " \
                  f"Meeting will be hosted on Zoom so make sure you have downloaded zoom app on your system. \n " \
                  f"Your Meeting link is {join_url}\n" \
                  f"Join the meeting link on {join_time} \n" \
                  f"Instructions:\n" \
                  f"Make sure you have the availability of camera.\n" \
                  f"Join the link before time to have better impression on the interviewer.\n" \
                  f"You may get disqualified if you remain absent on the allocated schedule of your interview.\n" \
                  f"Be prepared for the interview. Do your homework on things related to your rule in the internship.\n" \
                  f"Good Luck for the Interview"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[applicant_mail],
            fail_silently=False
            # html_message=msg_html,
        )

    def send_mail_to_organization(self, start_url, join_time):
        msg_html = render_to_string('internship_applicant_interview_mail.html')

        # get applicant list
        org_mail = self.get_org_mail()
        internship_name = self.get_internship_name()

        subject = "Internship Interview"
        message = f"Your {internship_name} has been scheduled on zoom so make sure you have downloaded zoom app on your system.\n " \
                  f"Your Meeting link is {start_url}\n" \
                  f"Start the meeting link on {join_time} \n"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[org_mail],
            fail_silently=False
            # html_message=msg_html,
        )

    def get_applicant_mail(self):
        user = User.objects.get(id=self.applicant_id)
        return user.email

    def get_internship_name(self):
        query = self.query_internship()
        return query.name

    def get_org_mail(self):
        query = self.query_internship()
        return query.user.uuid.email

    def query_internship(self):
        query = Internship.objects.get(id=self.internship_id)
        return query
