from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestViews(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_user_detail_view_returns_status_200(self):
        self.another_user = User.objects.create_user('another_user', 'another_user@lunch-economy.com', 'another_user')
        url = reverse('lunch_economy.apps.users.views.user_detail', args=(self.another_user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_detail_redirects_to_my_user_view(self):
        url = reverse('lunch_economy.apps.users.views.user_detail', args=(self.test_user.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('lunch_economy.apps.users.views.my_profile'))