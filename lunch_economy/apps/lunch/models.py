from django.contrib.auth.models import User
from django.db import models

from lunch_economy.apps.groups.models import LunchGroup


class Lunch(models.Model):
    leader = models.ForeignKey(User, related_name='leader+')
    group = models.ForeignKey(LunchGroup, related_name='group+')
    members = models.ManyToManyField(User, related_name='members+')
    date = models.DateField(auto_now_add=True)