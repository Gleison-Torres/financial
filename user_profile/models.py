from django.db import models
from django.contrib.auth.models import User


class EmailChangeRequest(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_change_request')
    new_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} -> {self.new_email}'