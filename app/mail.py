# import mail objects
from flask_mail import Mail, Message

# import mail extension
from app.extensions import mail

# logging
import logging
import traceback
# configure
logger = logging.getLogger(__name__)


def send_mail(subject, sender, recipients, text_body):
    try:
        # create message
        msg = Message(subject, sender=sender, recipients=recipients)
        # set message body
        msg.body = text_body
        # send message
        mail.send(msg)
    except Exception as e:
        # log
        logger.warning("sending mail failed with: %s" % str(e))
