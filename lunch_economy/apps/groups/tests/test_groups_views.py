from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from lunch_economy.apps.groups.models import LunchGroup


class TestViews(TestCase):
    def setUp(self):
        User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_my_groups_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.groups.views.my_groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_group_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.groups.views.create_group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_join_group_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.groups.views.join_group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_group_detail_returns_status_200(self):
        leader = User.objects.create_user('test_leader', 'test_leader@lunch-economy.com', 'test_leader')
        group = LunchGroup.objects.create(name="Test Group", leader=leader)
        url = reverse('lunch_economy.apps.groups.views.group_detail', args=(group.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)