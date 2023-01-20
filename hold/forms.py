from django.forms import ModelForm

from .models import Entity, Stake


# Create the form class.
class EntityForm(ModelForm):
    class Meta:
        model = Entity
        fields = ["name", "description", "wealth"]


class StakeForm(ModelForm):
    class Meta:
        model = Stake
        fields = ["owner", "owned", "stake"]
