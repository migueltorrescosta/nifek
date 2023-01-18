from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User

from .models import Card, Collection, UserCardScore


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
        self.permanent_collection_star = create_collection(
            "Test Star Collection", "Description of the test collection to star"
        )
        self.permanent_collection_unstar = create_collection(
            "Test Unstar Collection", "Description of the test collection to unstar"
        )
        self.permanent_collection_star.starred_by.remove(self.user)
        self.permanent_collection_unstar.starred_by.add(self.user)

    def test_http_get_homepage(self):
        response = self.client.get(reverse("cram:home"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_http_get_collection(self):
        relative_url = reverse(
            "cram:collection_detail", kwargs={"pk": self.permanent_collection.pk}
        )
        response = self.client.get(relative_url)
        self.assertEqual(response.status_code, 200)

    def test_http_star_entity(self):
        pk = self.permanent_collection_star.pk
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
        pk = self.permanent_collection_unstar.pk
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

    # def test_http_create_stake(self):
    #     relative_url = reverse("hold:stake")
    #     data = {
    #         "owner": self.permanent_entity.pk,
    #         "owned": self.permanent_entity_grandchild.pk,
    #         "stake": 0.1,
    #     }
    #     self.client.force_login(user=self.user)
    #     response = self.client.post(relative_url, follow=True, data=data)
    #     self.assertEqual(
    #         response.status_code, 200, "The post request failed for the entity creation"
    #     )
    #     self.assertTrue(
    #         Stake.objects.filter(
    #             owner__pk=data["owner"], owned__pk=data["owned"]
    #         ).exists(),
    #         "The post request was successful but no entity was created in the DB",
    #     )

    # def test_http_get_non_existing_entity(self):
    #     relative_url = reverse("hold:entity_detail", kwargs={"pk": 10**9 + 321})
    #     response = self.client.get(relative_url)
    #     self.assertEqual(response.status_code, 404)

    # def test_model_delete_entity(self):
    #     relative_url = reverse(
    #         "hold:entity_detail", kwargs={"pk": self.to_delete_entity.pk}
    #     )
    #     response = self.client.get(relative_url)
    #     self.assertEqual(
    #         response.status_code, 200, "This entity should exist due to the setUp"
    #     )
    #     relative_url = reverse(
    #         "hold:entity_detail", kwargs={"pk": self.to_delete_entity.pk}
    #     )
    #     self.to_delete_entity.delete()
    #     response = self.client.get(relative_url)
    #     self.assertEqual(
    #         response.status_code,
    #         404,
    #         "Although the model delete looked successful, the entity was not deleted",
    #     )

    # def test_model_entity_empty_recursive_assets(self):
    #     self.assertEqual(
    #         {s.pk for s in self.permanent_entity_grandchild.recursive_assets},
    #         set(),
    #         "Failed to correctly fetch recursive assets when none exist",
    #     )

    # def test_model_entity_empty_recursive_shareholders(self):
    #     self.assertEqual(
    #         {s.pk for s in self.permanent_entity.recursive_shareholders},
    #         set(),
    #         "Failed to correctly fetch recursive assets when none exist",
    #     )

    # def test_model_entity_direct_only_recursive_assets(self):
    #     self.assertEqual(
    #         {s.pk for s in self.permanent_entity_child.recursive_assets},
    #         {self.permanent_stake_child.pk},
    #         "Failed to correctly fetch recursive assets when none exist",
    #     )

    # def test_model_entity_direct_only_recursive_shareholders(self):
    #     self.assertEqual(
    #         {s.pk for s in self.permanent_entity_child.recursive_shareholders},
    #         {self.permanent_stake.pk},
    #         "Failed to correctly fetch recursive assets when none exist",
    #     )

    # def test_model_entity_indirect_recursive_assets(self):
    #     self.assertEqual(
    #         {s.pk for s in self.permanent_entity.recursive_assets},
    #         {self.permanent_stake.pk, self.permanent_stake_child.pk},
    #         "Failed to correctly fetch recursive assets when none exist",
    #     )

    # def test_model_entity_indirect_recursive_shareholders(self):
    #     self.assertEqual(
    #         {s.pk for s in self.permanent_entity_grandchild.recursive_shareholders},
    #         {self.permanent_stake.pk, self.permanent_stake_child.pk},
    #         "Failed to correctly fetch recursive assets when none exist",
    #     )
