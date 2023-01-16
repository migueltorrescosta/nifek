import random
from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    PROTECT,
    SET_NULL,
    DateTimeField,
    FloatField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    TextField,
)
from django.utils import timezone

from accounts.models import User

from .enums import RevisionStatus

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(1)]


class Collection(Model):
    owner = ForeignKey(
        User, null=False, on_delete=PROTECT, related_name="cram_collections"
    )
    starred_by = ManyToManyField(
        User, null=True, blank=True, related_name="starred_collections"
    )
    title = TextField()
    description = TextField()
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.title


class Card(Model):
    owner = ForeignKey(User, null=False, on_delete=PROTECT, related_name="cram_cards")
    collection = ForeignKey(
        Collection, on_delete=SET_NULL, null=True, related_name="cram_cards"
    )
    concept = TextField()
    description = TextField()
    success_rate = FloatField(
        null=False, blank=True, default=0.5, validators=PERCENTAGE_VALIDATOR
    )
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)

    class Meta:
        ordering = ["concept"]

    def __str__(self):
        return f"Card {self.concept} on Collection {self.collection.title}"


class UserCardScore(Model):
    user = ForeignKey(User, null=False, on_delete=CASCADE, related_name="cram_scores")
    card = ForeignKey(Card, null=False, on_delete=CASCADE, related_name="cram_scores")
    last_revision = IntegerField(
        choices=RevisionStatus.choices,
        default=RevisionStatus.AGAIN,
    )
    number_of_failed_revisions = IntegerField(validators=[MinValueValidator(0)])
    last_revision_timestamp = DateTimeField(null=False, auto_now_add=True)
    next_revision_timestamp = DateTimeField(null=False, auto_now_add=True)
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)

    class Meta:
        unique_together = (
            "user",
            "card",
        )

    def __str__(self):
        return f"Score for {self.user} on {self.card.concept}"

    def process_revision(self, revision: RevisionStatus) -> bool:
        last_interval = timezone.now() - self.last_revision_timestamp
        if revision == RevisionStatus.AGAIN:
            next_interval = timedelta(minutes=2)
            self.number_of_failed_revisions += 1
        elif last_interval <= timedelta(minutes=5):
            next_interval = timedelta(minutes=10)
        elif last_interval <= timedelta(minutes=15):
            next_interval = timedelta(hours=20)
        else:
            next_interval = (
                last_interval
                * max(1.3, 2.5 - 0.1 * self.number_of_failed_revisions)
                * random.uniform(1, 1.01)
            )
        self.last_revision_timestamp = timezone.now()
        self.next_revision_timestamp = timezone.now() + next_interval
        self.save()
        return True
