from django.db.models import (
    Model,
    ForeignKey,
    CharField,
    TextField,
    DateTimeField,
    FloatField,
    BigIntegerField,
    CASCADE,
    PROTECT,
)
from django.utils import timezone
from accounts.models import User
from .queries import stakes_raw_queries
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(1)]


class Entity(Model):
    submitted_by = ForeignKey(
        User, on_delete=PROTECT, related_name="hold_entities_submitted"
    )
    name = CharField("Name", max_length=240)
    description = TextField()
    wealth = BigIntegerField(
        help_text="Million EUR",
        blank=False,
        null=False,
        default=14.6 * 10**9,  # This corresponds to the S&P 500 Minimum
        validators=[MinValueValidator(0)],
    )
    founded_on = DateTimeField(blank=True, null=False, default=timezone.now)
    dissolved_on = DateTimeField(blank=True, null=True)
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)

    @property
    def recursive_stakes(self):
        return Stake.objects.raw(stakes_raw_queries(pk=self.pk, key="all"))

    @property
    def recursive_assets(self):
        return Stake.objects.raw(stakes_raw_queries(pk=self.pk, key="assets"))

    @property
    def recursive_shareholders(self):
        return Stake.objects.raw(stakes_raw_queries(pk=self.pk, key="shareholders"))

    class Meta:
        verbose_name_plural = "entities"

    def __str__(self):
        return self.name


class Stake(Model):
    submitted_by = ForeignKey(
        User, on_delete=PROTECT, related_name="hold_stakes_submitted"
    )
    owner = ForeignKey(Entity, on_delete=CASCADE, related_name="assets")
    owned = ForeignKey(Entity, on_delete=CASCADE, related_name="shareholders")
    stake = FloatField(null=False, blank=False, validators=PERCENTAGE_VALIDATOR)
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f"{self.owner} owns {self.stake*100 :.2f}% of {self.owned} "
