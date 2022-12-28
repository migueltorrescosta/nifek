from django.test import TestCase, Client
from .models import Thesis
from accounts.models import User
from django.urls import reverse


class ThesTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="test_user@nifek.com", username="test_user_for_thes_app"
        )
        create_thesis = lambda content: Thesis.objects.create(
            author=user, content=content
        )
        self.permanent_thesis = create_thesis("Test Permanent Thesis")
        self.to_delete_thesis = create_thesis("Test To Delete Thesis")
        self.client = Client()

    def test_http_get_homepage(self):
        response = self.client.get(reverse("thes:home"))
        self.assertEqual(response.status_code, 200)

    def test_http_get_thesis(self):
        relative_url = reverse(
            "thes:thesis_detail", kwargs={"pk": self.permanent_thesis.pk}
        )
        response = self.client.get(relative_url)
        self.assertEqual(response.status_code, 200)

    def test_http_get_non_existing_thesis(self):
        relative_url = reverse("thes:thesis_detail", kwargs={"pk": 10**9 + 321})
        response = self.client.get(relative_url)
        self.assertEqual(response.status_code, 404)

    def test_model_delete_thesis(self):
        relative_url = reverse(
            "thes:thesis_detail", kwargs={"pk": self.to_delete_thesis.pk}
        )
        response = self.client.get(relative_url)
        self.assertEqual(
            response.status_code, 200, "This Thesis should exist due to the setUp"
        )
        relative_url = reverse(
            "thes:thesis_detail", kwargs={"pk": self.to_delete_thesis.pk}
        )
        self.to_delete_thesis.delete()
        response = self.client.get(relative_url)
        self.assertEqual(
            response.status_code,
            404,
            "Although the model delete looked successful, the Thesis was not deleted",
        )
