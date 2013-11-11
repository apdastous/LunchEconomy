"""
Models for lunch_economy.apps.groups.
"""

from django.contrib.auth.models import Group, User
from django.db import models


class LunchGroup(Group):
    """
    Extends Django's built-in groups to add a field for leader.
    """
    leader = models.ForeignKey(User)

    @classmethod
    def create_for_user(cls, group_name, user):
        """
        Creates new group and adds user to it.
        Returns the group.
        """
        group = cls.objects.create(name=group_name, leader=user)
        user.groups.add(group)
        return group