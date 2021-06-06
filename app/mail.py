"""
    mail.py: contains function to send email
"""
# logging
import logging

# flask mail
from flask_mail import Message

# import mail extension
from app.extensions import mail


# configure
logger = logging.getLogger(__name__)


def send_mail(subject, sender, recipients, text_body):
    """
    send mail from string

    params:
        - subject: email subject
        - sender: email sender
        - recipients: send email to
        - text_body: email body
    """
    # create message
    msg = Message(subject, sender=sender, recipients=recipients)
    # set message body
    msg.body = text_body
    # send message
    mail.send(msg)
