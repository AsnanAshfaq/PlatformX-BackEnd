from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .models import FYP, Participant
from user.models import Organization, Student, User


class Mail:

    def __init__(self, fyp, applicant_id, data):
        self.fyp_id = fyp
        self.applicant_id = applicant_id
        self.data = data()

    def send_mail_to_applicant(self, join_url, join_time):
        # msg_html = render_to_string('internship_applicant_interview_mail.html')

        # get applicant list
        applicant_mail = self.get_applicant_mail()

        fyp_name = self.get_fyp_name()
        subject = "FYP Interview"
        message = f" Congratulations! You have been shortlisted for an online interview for {fyp_name}.\n " \
                  f"Your Meeting link on Zoom is {join_url}\n" \
                  f"Join the meeting link on {join_time} \n" \
            # f"Instructions:\n" \
        # f"Make sure you have the availability of camera.\n" \
        # f"Join the link before time to have better impression on the interviewer.\n" \
        # f"You may get disqualified if you remain absent on the allocated schedule of your interview.\n" \
        # f"Be prepared for the interview. Do your homework on things related to your rule in the internship.\n" \
        # f"Good Luck for the Interview"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[applicant_mail],
            fail_silently=False
            # html_message=msg_html,
        )

    def send_mail_to_organization(self, start_url, join_time):
        # get org mail
        fyp_name = self.get_fyp_name()
        org_mail = self.get_org_mail()

        subject = "FYP Interview"
        message = f" Your interview for ${fyp_name} has been scheduled on zoom.\n " \
                  f"Your Meeting link on Zoom is {start_url}\n" \
                  f"Date is {join_time}"
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

    def get_org_mail(self):
        query = self.query_fyp()
        return query.user.uuid.email

    def get_fyp_name(self):
        query = self.query_fyp()
        return query.name

    def query_fyp(self):
        query = FYP.objects.get(id=self.fyp_id)
        return query
