from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Card, Collection, UserCardScore
from .enums import RevisionStatus


class HoldTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test_cram_user@nifek.com", username="test_user_for_cram_app"
        )
        create_collection = lambda title, description: Collection.objects.create(
            owner=self.user, title=title, description=description
        )
        self.permanent_collection = create_collection(
            "Test Collection", "Description of the test collection"
        )
        self.permanent_collection_to_star = create_collection(
            "Test Star Collection", "Description of the test collection to star"
        )
        self.permanent_collection_to_unstar = create_collection(
            "Test Unstar Collection", "Description of the test collection to unstar"
        )
        self.permanent_starred_collection = create_collection(
            "Test Starred Collection", "Description of the test collection"
        )
        self.permanent_collection_to_test_card_creation = create_collection(
            "Test Collection to Create Card", "Description of the test collection"
        )
        self.permanent_starred_collection.starred_by.add(self.user)
        self.permanent_card = Card.objects.create(
            collection=self.permanent_starred_collection,
            concept="Test Card Concept",
            description="Test Card Description",
        )

        self.permanent_collection_to_star.starred_by.remove(self.user)
        self.permanent_collection_to_unstar.starred_by.add(self.user)

    def test_http_get_homepage_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("cram:home"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_http_get_homepage_logged_out(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cram:home"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_http_get_collection(self):
        relative_url = reverse(
            "cram:collection_detail", kwargs={"pk": self.permanent_collection.pk}
        )
        response = self.client.get(relative_url)
        self.assertEqual(response.status_code, 200)

    def test_http_star_entity(self):
        pk = self.permanent_collection_to_star.pk
        star_collection_url = reverse("cram:star_collection", kwargs={"pk": pk})
        self.client.force_login(user=self.user)

        self.assertTrue(
            not Collection.objects.filter(pk=pk).filter(starred_by=self.user).exists(),
            "The test_star_collection object should not be starred by the test user: the test was improperly setup",
        )
        response = self.client.post(star_collection_url, follow=True)
        self.assertEqual(
            response.status_code, 200, "The star endpoint returned a non 200 message"
        )
        self.assertTrue(
            Collection.objects.filter(pk=pk).filter(starred_by=self.user).exists(),
            "The star endpoint retrieved a successful message but did not work as expected",
        )
        response = self.client.post(star_collection_url, follow=True)
        self.assertEqual(
            response.status_code,
            200,
            "The star endpoint returned a non 200 message when restarred",
        )
        self.assertTrue(
            Collection.objects.filter(pk=pk).filter(starred_by=self.user).exists(),
            "The star endpoint retrieved a successful message but did not maintain the star on an already starred object",
        )

    def test_http_unstar_entity(self):
        pk = self.permanent_collection_to_unstar.pk
        unstar_collection_url = reverse("cram:unstar_collection", kwargs={"pk": pk})
        self.client.force_login(user=self.user)

        self.assertTrue(
            Collection.objects.filter(pk=pk).filter(starred_by=self.user).exists(),
            "The test_unstar_collection object should not be unstarred by the test user: the test was improperly setup",
        )
        response = self.client.post(unstar_collection_url, follow=True)
        self.assertEqual(
            response.status_code, 200, "The unstar endpoint returned a non 200 message"
        )
        self.assertTrue(
            not Collection.objects.filter(pk=pk).filter(starred_by=self.user).exists(),
            "The unstar endpoint retrieved a successful message but did not work as expected",
        )
        response = self.client.post(unstar_collection_url, follow=True)
        self.assertEqual(
            response.status_code,
            200,
            "The unstar endpoint returned a non 200 message when re-unstarred",
        )
        self.assertTrue(
            not Collection.objects.filter(pk=pk).filter(starred_by=self.user).exists(),
            "The unstar endpoint retrieved a successful message but did not maintain the 'unstar' on an already starred object",
        )

    def test_submit_card_review(self):
        self.client.force_login(user=self.user)
        self.assertTrue(
            not UserCardScore.objects.filter(card=self.permanent_card).exists(),
            "The test card should not have a score for the test user: the test",
        )
        get_initial_review_url = reverse("cram:review")
        response = self.client.get(get_initial_review_url, follow=True)
        self.assertEqual(
            response.status_code,
            200,
            "The initial review endpoint returned a non HTTP 200/success message",
        )
        self.assertTrue(
            UserCardScore.objects.filter(card=self.permanent_card).exists(),
            "The initial review endpoint retrieved a successful message but did not create a UserCardScore object",
        )
        user_card_score = UserCardScore.objects.get(
            card=self.permanent_card, user=self.user
        )
        submit_card_review_url = reverse(
            "cram:submit_review", kwargs={"pk": user_card_score.pk}
        )
        response = self.client.post(
            submit_card_review_url,
            data={"last_revision": RevisionStatus.AGAIN},
            follow=False,
        )
        self.assertEqual(
            response.status_code,
            302,
            "The submit card review endpoint returned a non HTTP 302/redirect message",
        )
        response = self.client.get(get_initial_review_url, follow=True)
        self.assertEqual(
            response.status_code,
            200,
            "The initial review endpoint returned a non HTTP 200/success message",
        )
        response = self.client.post(
            submit_card_review_url,
            data={"last_revision": RevisionStatus.EASY},
            follow=False,
        )
        self.assertEqual(
            response.status_code,
            302,
            "The submit card review endpoint returned a non HTTP 302/redirect message",
        )

    def test_create_collection(self):
        self.client.force_login(self.user)
        create_collection_url = reverse("cram:collections")
        collection_title = "Test Collection Creation"
        response = self.client.post(
            create_collection_url,
            data={
                "title": collection_title,
                "description": "Description of the test collection",
            },
            follow=True,
        )
        self.assertEqual(
            response.status_code,
            200,
            "The create collection endpoint returned a non HTTP 200/success message",
        )
        self.assertTrue(
            Collection.objects.filter(title=collection_title).exists(),
            "The create collection endpoint retrieved a successful message but did not create a collection",
        )

    def test_create_card(self):
        self.client.force_login(self.user)
        create_card_url = reverse(
            "cram:collection_detail",
            kwargs={"pk": self.permanent_collection_to_test_card_creation.pk},
        )
        card_concept = "Test Card Creation"
        response = self.client.post(
            create_card_url,
            data={"concept": card_concept, "description": "Back of the test card"},
            follow=True,
        )
        self.assertEqual(
            response.status_code,
            200,
            "The create card endpoint returned a non HTTP 200/success message",
        )
        self.assertTrue(
            Card.objects.filter(concept=card_concept).exists(),
            "The create card endpoint retrieved a successful message but did not create a card",
        )
