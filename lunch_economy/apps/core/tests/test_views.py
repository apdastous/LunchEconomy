from django.core.urlresolvers import reverse
from django.test import TestCase


class TestViews(TestCase):
    def test_home_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.core.views.home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)