from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import email_change_token


def send_email_change_confirmation(request, email_change_request):

    uid = urlsafe_base64_encode(
        force_bytes(email_change_request.pk)
    )

    token = email_change_token.make_token(
        email_change_request
    )

    confirmation_link = request.build_absolute_uri(
        reverse('confirm_email_change', kwargs={'uidb64': uid, 'token': token}))

    send_mail(
        subject='Confirme a alteração do seu e-mail',
        message=(
            'Para confirmar seu novo endereço de e-mail, '
            f'acesse o link abaixo:\n\n{confirmation_link}'
        ),
        from_email=None,
        recipient_list=[
            email_change_request.new_email
        ],
    )