from django.forms import ModelForm
from .models import Entity

# Create the form class.
class EntityForm(ModelForm):
    class Meta:
        model = Entity
        fields = ["name", "description"]
