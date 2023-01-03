from django.test import TestCase, Client
from .models import Entity, Stake
from accounts.models import User
from django.urls import reverse


class HoldTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test_user@nifek.com", username="test_user_for_hold_app"
        )
        create_entity = lambda name, description: Entity.objects.create(
            submitted_by=self.user, name=name, description=description
        )
        self.permanent_entity = create_entity("Test Entity A", "Description A")
        self.permanent_entity_child = create_entity("Test Entity A1", "Description A1")
        self.permanent_entity_grandchild = create_entity(
            "Test Entity A2", "Description A2"
        )
        self.permanent_stake = Stake.objects.create(
            submitted_by=self.user,
            owner=self.permanent_entity,
            owned=self.permanent_entity_child,
            stake=0.5,
        )
        self.permanent_stake_child = Stake.objects.create(
            submitted_by=self.user,
            owner=self.permanent_entity_child,
            owned=self.permanent_entity_grandchild,
            stake=0.5,
        )
        self.to_delete_entity = create_entity("Test Entity A", "Description B")
        self.client = Client()

    def test_http_get_homepage(self):
        response = self.client.get(reverse("hold:home"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_http_get_entity(self):
        relative_url = reverse(
            "hold:entity_detail", kwargs={"pk": self.permanent_entity.pk}
        )
        response = self.client.get(relative_url)
        self.assertEqual(response.status_code, 200)

    def test_http_create_entity(self):
        relative_url = reverse("hold:entity")
        data = {
            "name": "Entity Created During Tests",
            "description": "mocked description",
            "wealth": 14.6 * 10**9,
        }
        self.client.force_login(user=self.user)
        response = self.client.post(relative_url, follow=True, data=data)
        self.assertEqual(
            response.status_code, 200, "The post request failed for the entity creation"
        )
        self.assertTrue(
            Entity.objects.filter(name=data["name"]).exists(),
            "The post request was successful but no entity was created in the DB",
        )

    def test_http_create_stake(self):
        relative_url = reverse("hold:stake")
        data = {
            "owner": self.permanent_entity.pk,
            "owned": self.permanent_entity_grandchild.pk,
            "stake": 0.1,
        }
        self.client.force_login(user=self.user)
        response = self.client.post(relative_url, follow=True, data=data)
        self.assertEqual(
            response.status_code, 200, "The post request failed for the entity creation"
        )
        self.assertTrue(
            Stake.objects.filter(
                owner__pk=data["owner"], owned__pk=data["owned"]
            ).exists(),
            "The post request was successful but no entity was created in the DB",
        )

    def test_http_get_non_existing_entity(self):
        relative_url = reverse("hold:entity_detail", kwargs={"pk": 10**9 + 321})
        response = self.client.get(relative_url)
        self.assertEqual(response.status_code, 404)

    def test_model_delete_entity(self):
        relative_url = reverse(
            "hold:entity_detail", kwargs={"pk": self.to_delete_entity.pk}
        )
        response = self.client.get(relative_url)
        self.assertEqual(
            response.status_code, 200, "This entity should exist due to the setUp"
        )
        relative_url = reverse(
            "hold:entity_detail", kwargs={"pk": self.to_delete_entity.pk}
        )
        self.to_delete_entity.delete()
        response = self.client.get(relative_url)
        self.assertEqual(
            response.status_code,
            404,
            "Although the model delete looked successful, the entity was not deleted",
        )

    def test_model_entity_empty_recursive_assets(self):
        self.assertEqual(
            {s.pk for s in self.permanent_entity_grandchild.recursive_assets},
            set(),
            "Failed to correctly fetch recursive assets when none exist",
        )

    def test_model_entity_empty_recursive_shareholders(self):
        self.assertEqual(
            {s.pk for s in self.permanent_entity.recursive_shareholders},
            set(),
            "Failed to correctly fetch recursive assets when none exist",
        )

    def test_model_entity_direct_only_recursive_assets(self):
        self.assertEqual(
            {s.pk for s in self.permanent_entity_child.recursive_assets},
            {self.permanent_stake_child.pk},
            "Failed to correctly fetch recursive assets when none exist",
        )

    def test_model_entity_direct_only_recursive_shareholders(self):
        self.assertEqual(
            {s.pk for s in self.permanent_entity_child.recursive_shareholders},
            {self.permanent_stake.pk},
            "Failed to correctly fetch recursive assets when none exist",
        )

    def test_model_entity_indirect_recursive_assets(self):
        self.assertEqual(
            {s.pk for s in self.permanent_entity.recursive_assets},
            {self.permanent_stake.pk, self.permanent_stake_child.pk},
            "Failed to correctly fetch recursive assets when none exist",
        )

    def test_model_entity_indirect_recursive_shareholders(self):
        self.assertEqual(
            {s.pk for s in self.permanent_entity_grandchild.recursive_shareholders},
            {self.permanent_stake.pk, self.permanent_stake_child.pk},
            "Failed to correctly fetch recursive assets when none exist",
        )
