from random import randint

from django.db import models
from django.db.models import Count


class Quote(models.Model):
    """
    Quotes are loaded from core.fixtures and displayed on the homepage.
    """
    author = models.CharField(max_length=120)
    text = models.CharField(max_length=250)

    @classmethod
    def get_random(cls):
        """
        Returns a random Quote object.
        """
        count = cls.objects.count()
        random_index = randint(0, count - 1)
        return cls.objects.all()[random_index]