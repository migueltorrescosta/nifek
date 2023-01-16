from django.test import TestCase
from accounts.models import User
from django.urls import reverse


class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test_user@nifek.com", username="test_user_for_hold_app"
        )

    def test_login_page_exists(self):
        response = self.client.get(reverse("magiclink:login"))
        self.assertEqual(response.status_code, 200)
