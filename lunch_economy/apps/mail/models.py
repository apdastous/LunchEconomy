from django.contrib.auth.models import User
from django.db import models


class Mail(models.Model):
    sender = models.ForeignKey(User, related_name="sender+")
    recipient = models.ForeignKey(User, related_name="recipient+")
    text = models.TextField()
    sent = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)

    @classmethod
    def system_notification(cls, recipient, text):
        """
        Sends a message to a recipient from the system user.
        """
        system_user = User.objects.get(pk=100)
        cls.objects.create(
            sender=system_user,
            recipient=recipient,
            text=text
        )