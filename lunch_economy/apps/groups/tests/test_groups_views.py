"""
Unit tests for lunch_economy.apps.group.views.
"""

from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.core.urlresolvers import reverse
from django.test import TestCase

from lunch_economy.apps.groups.models import LunchGroup
from lunch_economy.apps.mail.models import Mail


class TestMyGroupsView(TestCase):
    """
    Unit tests for the 'my_group' view.
    """

    def setUp(self):
        """
        All views have the login_required decorator, so let's log in a test user.
        """
        self.test_user = User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_view_returns_status_200(self):
        """
        A get with no params returns status 200.
        """
        url = reverse('lunch_economy.apps.groups.views.my_groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCreateGroupView(TestCase):
    """
    Unit tests for the 'create_group' view.
    """

    def setUp(self):
        """
        All views have the login_required decorator, so let's log in a test user.
        """
        self.test_user = User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_view_returns_status_200(self):
        """
        A get with no params returns status 200.
        """
        url = reverse('lunch_economy.apps.groups.views.create_group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_with_valid_data_redirects_to_group_detail(self):
        """
        POSTing with valid data redirects to the group_detail view.
        """
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        response = self.client.post(url, data)
        group = LunchGroup.objects.get(name="Test Group")
        redirect_url = reverse('lunch_economy.apps.groups.views.group_detail', args=(group.id,))
        self.assertRedirects(response, redirect_url)

    def test_post_with_valid_data_creates_group_model(self):
        """
        POSTing with valid data creates the LunchGroup model.
        """
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        self.client.post(url, data)
        group = LunchGroup.objects.get(name="Test Group")
        self.assertEqual(group.name, data['group-name'])

    def test_post_with_valid_data_sets_user_as_group_leader(self):
        """
        POSTing with valid data adds the user to the LunchGroup leader field.
        """
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        self.client.post(url, data)
        group = LunchGroup.objects.get(name="Test Group")
        self.assertEqual(group.leader, self.test_user)

    def test_post_with_valid_data_adds_user_to_group(self):
        """
        POSTing with valid data adds the user to the LunchGroup group.
        """
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        self.client.post(url, data)
        group = LunchGroup.objects.get(name="Test Group")
        self.assertTrue(self.test_user.groups.filter(name=group.name).exists())

    def test_post_with_group_name_already_taken_returns_error_message(self):
        """
        POSTing with a group name that is already used results in error message.
        """
        leader = User.objects.create_user('test_leader', 'test_leader@lunch-economy.com', 'test_leader')
        LunchGroup.objects.create(name="Test Group", leader=leader)
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        response = self.client.post(url, data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, constants.ERROR)

    def test_post_with_group_name_already_taken_redirects_to_create_group(self):
        """
        POSTing with a group name that is already used redirects to the create_group view.
        """
        leader = User.objects.create_user('test_leader', 'test_leader@lunch-economy.com', 'test_leader')
        LunchGroup.objects.create(name="Test Group", leader=leader)
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, url)

    def test_user_recieves_system_notification_after_creating_group(self):
        """
        POSTing with valid data results in mail being created.
        """
        url = reverse('lunch_economy.apps.groups.views.create_group')
        data = {'group-name': "Test Group"}
        self.client.post(url, data)
        mail = Mail.objects.get(recipient=self.test_user)
        self.assertIn(data['group-name'], mail.text)


class TestJoinGroupView(TestCase):
    """
    Unit tests for the 'join_group' view.
    """

    def setUp(self):
        """
        All views have the login_required decorator, so let's log in a test user.
        """
        self.test_user = User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_view_returns_status_200(self):
        """
        A get with no params returns status 200.
        """
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
    """
    Unit tests for the group_detail view.
    """
    def setUp(self):
        """
        All views have the login_required decorator, so let's log in a test user.
        """
        self.test_user = User.objects.create_user('test_user', 'test_user@lunch-economy.com', 'test_user')
        self.client.login(username='test_user', password='test_user')

    def test_group_detail_returns_status_200(self):
        """
        Adds a user and creates a group with that user as leader.
        A get with no params returns status 200.
        """
        leader = User.objects.create_user('test_leader', 'test_leader@lunch-economy.com', 'test_leader')
        group = LunchGroup.objects.create(name="Test Group", leader=leader)
        url = reverse('lunch_economy.apps.groups.views.group_detail', args=(group.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
