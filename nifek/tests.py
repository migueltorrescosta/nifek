from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class ThesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test_user@nifek.com", username="test_user_for_thes_app"
        )

    def test_http_get_homepage_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_http_get_homepage_logged_in(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
