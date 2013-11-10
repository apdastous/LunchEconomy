from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestAnonymousAccess(TestCase):
    def setUp(self):
        self.home_url = reverse('lunch_economy.apps.core.views.home')

    def test_anonymous_user_can_access_home(self):
        url = reverse('lunch_economy.apps.core.views.home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestUserAccess(TestCase):
    def setUp(self):
        User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_authorized_user_can_access_home(self):
        url = reverse('lunch_economy.apps.core.views.home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
