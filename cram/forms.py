from django.forms import (
    ModelForm,
    ChoiceField,
    CheckboxSelectMultiple,
    RadioSelect,
)
from .models import UserCardScore
from .enums import RevisionStatus

# Create the form class.
class UserCardScoreForm(ModelForm):

    last_revision = ChoiceField(
        required=True, choices=RevisionStatus.choices, label="memorability"
    )

    class Meta:
        model = UserCardScore
        fields = ["last_revision"]
