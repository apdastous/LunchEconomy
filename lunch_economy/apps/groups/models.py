from django.contrib.auth.models import Group, User
from django.db import models


class LunchGroup(Group):
    leader = models.ForeignKey(User)
