from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestViews(TestCase):
    def setUp(self):
        User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_inbox_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.mail.views.inbox')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
