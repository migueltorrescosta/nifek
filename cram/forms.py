from django.forms import ChoiceField, ModelForm, CharField

from .enums import RevisionStatus
from .models import Card, Collection, UserCardScore


# Create the form class.
class UserCardScoreForm(ModelForm):

    last_revision = ChoiceField(
        required=True, choices=RevisionStatus.choices, label="memorability"
    )

    class Meta:
        model = UserCardScore
        fields = ["last_revision"]


class CardForm(ModelForm):

    concept = CharField()

    class Meta:
        model = Card
        fields = ["concept", "description"]


class CollectionForm(ModelForm):

    title = CharField()

    class Meta:
        model = Collection
        fields = ["title", "description"]
