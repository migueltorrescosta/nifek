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
from .exceptions import NoNextCardException

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(1)]


class Collection(Model):
    owner = ForeignKey(
        User, null=False, on_delete=PROTECT, related_name="cram_collections"
    )
    starred_by = ManyToManyField(User, blank=True, related_name="starred_collections")
    title = TextField()
    description = TextField()
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.title


class Card(Model):
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

    def update_success_rate(self) -> bool:
        numerator = self.cram_scores.filter(last_revision=RevisionStatus.AGAIN).count()
        denominator = self.cram_scores.count()
        self.success_rate = (numerator + 1) / (denominator + 2)
        self.save()
        return True

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
        last_interval = max(last_interval, timedelta(seconds=1))
        if revision == RevisionStatus.AGAIN:
            self.number_of_failed_revisions += 1
            next_interval = timedelta(minutes=5)
        else:
            initial_intervals = [1200, 60, 5, 0]  # in minutes
            while initial_intervals and last_interval <= timedelta(
                minutes=initial_intervals.pop() * 1.5
            ):
                pass
            if initial_intervals:
                next_interval = timedelta(minutes=initial_intervals.pop())
            else:
                next_interval = (
                    last_interval
                    * max(1.3, 2.5 - 0.1 * self.number_of_failed_revisions)
                    * random.uniform(1, 1.01)
                )
        self.last_revision = revision
        self.last_revision_timestamp = timezone.now()
        self.next_revision_timestamp = timezone.now() + next_interval
        self.save()
        self.card.update_success_rate()
        return True

    @classmethod
    def get_user_next_card_score(self, user: User) -> "Card":
        if not Collection.objects.filter(starred_by=user).exists():
            raise NoNextCardException(
                "You have no collections starred. Star a collection to start learning."
            )

        if not Card.objects.filter(collection__starred_by=user).exists():
            raise NoNextCardException(
                "You have no starred collections with at least one card. Star a collection to start learning."
            )

        next_user_card_score = (
            UserCardScore.objects.filter(user=user)
            .filter(next_revision_timestamp__lte=timezone.now())
            .filter(card__collection__starred_by=user)
            .order_by("next_revision_timestamp")
            .first()
        )

        if next_user_card_score is None:
            new_card = (
                Card.objects.filter(collection__starred_by=user)
                .filter(collection__starred_by=user)
                .exclude(cram_scores__user=user)
                .order_by("-success_rate")
                .first()
            )
            n_cards_being_learnt = (
                UserCardScore.objects.filter(user=user)
                .filter(last_revision=RevisionStatus.AGAIN)
                .filter(card__collection__starred_by=user)
                .count()
            )
            if new_card is None or n_cards_being_learnt > 2:
                next_card_timestamp = (
                    UserCardScore.objects.filter(user=user)
                    .filter(next_revision_timestamp__gte=timezone.now())
                    .order_by("next_revision_timestamp")
                    .first()
                ).next_revision_timestamp
                timedelta = next_card_timestamp - timezone.now()
                minutes = 1 + int(timedelta.total_seconds() / 60)
                if minutes <= 60:
                    time = f"{minutes} minute{'s' if minutes != 1 else ''}"
                else:
                    hours = 1 + int(minutes / 3600)
                    time = f"{hours} hour{'s' if hours != 1 else ''}"
                cards_to_revise = {
                    c["card__concept"]
                    for c in UserCardScore.objects.filter(user=user)
                    .filter(last_revision=RevisionStatus.AGAIN)
                    .filter(card__collection__starred_by=user)
                    .values("card__concept")
                }
                raise NoNextCardException(
                    f"You have no cards to review at the moment. Come back in {time}. The cards you most need to revise are: {', '.join(cards_to_revise)}"
                )

            else:
                next_user_card_score = UserCardScore.objects.create(
                    card=new_card,
                    user=user,
                    last_revision=RevisionStatus.AGAIN,
                    number_of_failed_revisions=0,
                )
                next_user_card_score.save()

        return next_user_card_score
