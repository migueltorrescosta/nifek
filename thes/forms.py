from django.forms import ModelForm
from .models import Thesis

# Create the form class.
class ThesisForm(ModelForm):
    class Meta:
        model = Thesis
        fields = ["content"]
        labels = {"content": ""}
