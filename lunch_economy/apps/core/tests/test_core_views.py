from django.core.urlresolvers import reverse
from django.test import TestCase


class TestViews(TestCase):
    def test_home_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.core.views.home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_contains_quote(self):
        url = reverse('lunch_economy.apps.core.views.home')
        response = self.client.get(url)
        self.assertTrue(response.context['quote'])
