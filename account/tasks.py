from celery.decorators import task
from celery.utils.log import get_task_logger

from .email import send_registration_email, send_transaction_email

logger = get_task_logger(__name__)


@task(name="send_registration_email_task")
def send_registration_email_task(name, username, email):
    logger.info("Sent resgistration email")
    return send_registration_email(name, username, email)

@task(name="send_transaction_email_task")
def send_transaction_email_task(email, type, transaction_id, payment_gateway, amount):
    logger.info("Sent transaction email")
    return send_transaction_email(email, type, transaction_id, payment_gateway, amount)
