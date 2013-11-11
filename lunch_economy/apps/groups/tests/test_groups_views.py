from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from lunch_economy.apps.groups.models import LunchGroup


class TestMyGroupsView(TestCase):
    def setUp(self):
        User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.groups.views.my_groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCreateGroupView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.groups.views.create_group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_with_valid_data_redirects_to_group_detail(self):
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        response = self.client.post(url, data)
        group = LunchGroup.objects.get(name="Test Group")
        self.assertRedirects(response, reverse('lunch_economy.apps.groups.views.group_detail', args=(group.id,)))

    def test_post_with_valid_data_creates_group_model(self):
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        self.client.post(url, data)
        group = LunchGroup.objects.get(name="Test Group")
        self.assertEqual(group.name, data['group-name'])

    def test_post_with_valid_data_sets_user_as_group_leader(self):
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        self.client.post(url, data)
        group = LunchGroup.objects.get(name="Test Group")
        self.assertEqual(group.leader, self.test_user)

    def test_post_with_valid_data_adds_user_to_group(self):
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        self.client.post(url, data)
        group = LunchGroup.objects.get(name="Test Group")
        self.assertTrue(self.test_user.groups.filter(name=group.name).exists())

    def test_post_with_group_name_already_taken_returns_error_message(self):
        leader = User.objects.create_user('test_leader', 'test_leader@lunch-economy.com', 'test_leader')
        LunchGroup.objects.create(name="Test Group", leader=leader)
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        response = self.client.post(url, data, follow=True)
        self.assertContains(response, "already taken")

    def test_post_with_group_name_already_taken_redirects_to_create_group(self):
        leader = User.objects.create_user('test_leader', 'test_leader@lunch-economy.com', 'test_leader')
        LunchGroup.objects.create(name="Test Group", leader=leader)
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, url)


class TestJoinGroupView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_view_returns_status_200(self):
        url = reverse('lunch_economy.apps.groups.views.join_group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_groups_list_is_populated(self):
        leader = User.objects.create_user('test_leader', 'test_leader@lunch-economy.com', 'test_leader')
        group = LunchGroup.objects.create(name="Test Group", leader=leader)
        url = reverse('lunch_economy.apps.groups.views.join_group')
        response = self.client.get(url)
        self.assertContains(response, group)

    def test_groups_list_does_not_contain_users_groups(self):
        group = LunchGroup.objects.create(name="Test Group", leader=self.test_user)
        self.test_user.groups.add(group)
        url = reverse('lunch_economy.apps.groups.views.join_group')
        response = self.client.get(url)
        self.assertNotContains(response, group)


class TestGroupDetailView(TestCase):
    def setUp(self):
        User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_group_detail_returns_status_200(self):
        leader = User.objects.create_user('test_leader', 'test_leader@lunch-economy.com', 'test_leader')
        group = LunchGroup.objects.create(name="Test Group", leader=leader)
        url = reverse('lunch_economy.apps.groups.views.group_detail', args=(group.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)