from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailChangeTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, email_change_request, timestamp):
        return (
            f'{email_change_request.pk}'
            f'{email_change_request.user.pk}'
            f'{email_change_request.new_email}'
            f'{timestamp}'
        )


email_change_token = EmailChangeTokenGenerator()