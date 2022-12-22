from django.forms import ModelForm
from thes.models import Thesis

# Create the form class.
class ThesisForm(ModelForm):
    class Meta:
        model = Thesis
        fields = ["content"]
