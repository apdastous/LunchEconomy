from django.test import TestCase
from lunch_economy.apps.core.models import Quote


class TestModels(TestCase):
    def test_quote_random_method(self):
        quote = Quote.get_random()
        self.assertIsNotNone(quote)
