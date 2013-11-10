from django.core.urlresolvers import reverse
from django.test import TestCase


class TestAccess(TestCase):
    def setUp(self):
        self.home_url = reverse('lunch_economy.apps.core.views.home')

    def test_anonymous_user_cannot_access_inbox(self):
        url = reverse('lunch_economy.apps.mail.views.inbox')
        response = self.client.get(url)
        self.assertRedirects(response, self.home_url + "?next=" + url)
