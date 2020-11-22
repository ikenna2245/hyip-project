from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_registration_email(name, username, email):
    context = {
        'name': name,
        'username': username,
        'email': email,
    }
    email_subject = 'Welcome to CoinInvest'
    email_body = render_to_string('account/email_message.html', context)
    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    return email.send(fail_silently=False)


def send_transaction_email(email, type, transaction_id, payment_gateway, amount):
    context = {
        'type': type,
        'transaction_id': transaction_id,
        'payment_gateway': payment_gateway,
        'amount': amount
    }
    email_subject = 'Latest Transaction on CoinInvest'
    email_body = render_to_string('account/email_transaction.html', context)
    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    return email.send(fail_silently=False)
