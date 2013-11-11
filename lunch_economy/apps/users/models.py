from django.contrib.auth.models import User
from django.db import models

from lunch_economy.apps.groups.models import LunchGroup


class Debt(models.Model):
    group = models.ForeignKey(LunchGroup)
    debtor = models.ForeignKey(User, related_name="debtor+")
    debtee = models.ForeignKey(User, related_name="debtee+")
    amount = models.IntegerField(default=0)