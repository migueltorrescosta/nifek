from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse

from .models import Entity, Stake

# from .forms import ThesisForm


def home(request):
    """Selects a random entity to view"""
    entity = Entity.objects.order_by("?").first()
    url = reverse("hold:entity_detail", kwargs={"pk": entity.pk})
    # Render the HTML template index.html with the data in the context variable
    return redirect(url)


class EntityDetail(generic.DetailView):
    model = Entity
    template_name = "hold/entity_detail.html"

    def get_context_data(self, object, **kwargs):
        context = super(EntityDetail, self).get_context_data(**kwargs)
        relevant_stakes = object.recursive_stakes
        context["entity_list"] = Entity.objects.order_by("name")
        context["stakes"] = Stake.objects.filter(
            pk__in=[s.id for s in relevant_stakes]
        ).order_by("-stake")
        # context["messages"] = self.get("messages", [])
        return context
