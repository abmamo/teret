# import mail objects
from flask_mail import Mail, Message

# import mail extension
from app.extensions import mail


def send_mail(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)
