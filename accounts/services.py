from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.token import account_activation_token


def send_activation_email(request, user):
    current_site = get_current_site(request)

    subject = 'Ative sua conta'

    message = render_to_string(
        'emails/account_activation.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
    )

    email = EmailMessage(
        subject=subject,
        body=message,
        to=[user.email]
    )

    email.content_subtype = 'html'
    email.send()
