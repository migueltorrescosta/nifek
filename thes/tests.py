from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User

from .models import Tag, Thesis


class ThesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test_user@nifek.com", username="test_user_for_thes_app"
        )
        create_thesis = lambda content: Thesis.objects.create(
            author=self.user, content=content
        )
        self.permanent_thesis = create_thesis("Test Permanent Thesis")
        self.to_delete_thesis = create_thesis("Test To Delete Thesis")
        self.client = Client()

    def test_http_get_homepage(self):
        response = self.client.get(reverse("thes:home"))
        self.assertEqual(response.status_code, 200)

    def test_http_get_thesis_list_with_query(self):
        relative_url = reverse("thes:home") + "?q=Test"
        response = self.client.get(relative_url)
        self.assertEqual(response.status_code, 200)

    def test_http_get_thesis(self):
        relative_url = reverse(
            "thes:thesis_detail", kwargs={"pk": self.permanent_thesis.pk}
        )
        response = self.client.get(relative_url)
        self.assertEqual(response.status_code, 200)

    def test_http_create_thesis(self):
        relative_url = reverse("thes:home")
        data = {
            "content": "Thesis created during tests",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(relative_url, follow=True, data=data)
        self.assertEqual(
            response.status_code, 200, "The post request failed for the thesis creation"
        )
        self.assertTrue(
            Thesis.objects.filter(content=data["content"]).exists(),
            "The post request was successful but no thesis was created in the DB",
        )

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

    def test_http_tag_thesis(self):
        relative_url = reverse(
            "thes:tag_thesis", kwargs={"pk": self.permanent_thesis.pk}
        )
        data = {
            "property": "TestingTag",
        }
        self.client.force_login(user=self.user)
        self.assertFalse(
            Tag.objects.filter(property__text=data["property"]).exists(),
            "The desired Tag already exists even before the HTTP request was made",
        )
        response = self.client.post(relative_url, follow=True, data=data)
        self.assertEqual(
            response.status_code, 200, "The post request failed for the tag creation"
        )
        self.assertTrue(
            Tag.objects.filter(property__text=data["property"]).exists(),
            "The post request was successful but no tag was created in the DB",
        )

    def test_http_tag_thesis_with_too_long_test(self):
        relative_url = reverse(
            "thes:tag_thesis", kwargs={"pk": self.permanent_thesis.pk}
        )
        data = {
            "property": "TestingTagThatIsTooLongToBeAccepted",
        }
        self.client.force_login(user=self.user)
        self.assertFalse(
            Tag.objects.filter(property__text=data["property"]).exists(),
            "The desired Tag already exists even before the HTTP request was made",
        )
        response = self.client.post(relative_url, follow=True, data=data)
        self.assertEqual(
            response.status_code,
            200,
            "The post request did not return a 400 error even though the tag was too long!",
        )
        self.assertFalse(
            Tag.objects.filter(property__text=data["property"]).exists(),
            "The tag was created although it shouldn't",
        )
