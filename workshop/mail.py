from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


def workshop_participant_invitation_mail():
    msg_html = render_to_string('workshop_join_invitation_mail.html')
    send_mail(
        subject="Workshop invitation",
        message="Workshop invitation",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["18asnan@gmail.com"],
        html_message=msg_html,
    )


def workshop_organizer_invitation_mail():
    pass
