from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from lunch_economy.apps.mail.models import Mail


class TestAccess(TestCase):
    def setUp(self):
        self.home_url = reverse('lunch_economy.apps.core.views.home')

    def test_anonymous_user_cannot_access_inbox(self):
        url = reverse('lunch_economy.apps.mail.views.inbox')
        response = self.client.get(url)
        self.assertRedirects(response, self.home_url + "?next=" + url)

    def test_user_cannot_read_others_mail(self):
        test_user_1 = User.objects.create_user('test_user_1', 'test_user_1@lunch-economy.com', 'test_user_1')
        test_user_2 = User.objects.create_user('test_user_2', 'test_user_2@lunch-economy.com', 'test_user_2')
        User.objects.create_user('spy_user', 'spy_user@lunch-economy.com', 'spy_user')
        mail = Mail.objects.create(
            sender=test_user_1,
            recipient=test_user_2,
            text="I hope nobody else can read this!"
        )

        url = reverse('lunch_economy.apps.mail.views.mail_detail', args=(mail.id,))
        self.client.login(username='spy_user', password='spy_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
