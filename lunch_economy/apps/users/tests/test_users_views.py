from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestViews(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_user_detail_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.users.views.user_detail', args=(self.test_user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)