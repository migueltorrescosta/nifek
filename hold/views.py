from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from .forms import EntityForm, StakeForm
from .models import Entity, Stake
from .settings import MAXIMUM_ENTITY_VALUE


def home(request):
    """Selects a random entity to view"""
    entity = Entity.objects.order_by("?").first()
    url = reverse("hold:entity_detail", kwargs={"pk": entity.pk})
    # Render the HTML template index.html with the data in the context variable
    return redirect(url)


def post_entity(request):

    if not request.user.is_authenticated:
        return _show_error_util(request, "You cannot add an Entity without logging in")
    form = EntityForm(data=request.POST)

    if not form.is_valid():
        return _show_error_util(request, "The submitted Entity is invalid")

    if float(form["wealth"].value()) > MAXIMUM_ENTITY_VALUE:
        return _show_error_util(
            request, "We cannot submit entities with over 5 Trillion EUR"
        )

    try:
        entity = form.save(commit=False)
        entity.submitted_by = request.user
        entity.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully submitted entity {entity.name} by {request.user.username}",
        )
    except:
        return _show_error_util(request, f"Failed to create entity {entity.name}")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("hold:home")))


def post_stake(request):

    if not request.user.is_authenticated:
        return _show_error_util(request, "You cannot add Stakes without logging in")

    form = StakeForm(data=request.POST)

    if not form.is_valid():
        return _show_error_util(request, "The submitted Stake submission is invalid")

    try:
        stake = form.save(commit=False)
        if stake.owner == stake.owned:
            return _show_error_util(
                request, f"{stake.owner} cannot be the owner and owned simultaneously."
            )
        if Stake.objects.filter(owner=stake.owner, owned=stake.owned).exists():
            return _show_error_util(
                request,
                f"A stake already exists where {stake.owner} owns {stake.owned}",
            )
        if stake.owner.id in [s.owned_id for s in stake.owned.recursive_assets]:
            return _show_error_util(
                request,
                f"{stake.owned} already owns part of {stake.owner}, which would create a circular dependency. We are not smart enough to handle this yet",
            )
        stake.submitted_by = request.user
        stake.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully submitted {100* stake.stake:.1f}% stake of {stake.owned.name} by {stake.owner.name}, by {stake.submitted_by.username}",
        )
    except:
        return _show_error_util(request, "Failed to create stake")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("hold:home")))


class EntityDetail(generic.DetailView):
    model = Entity
    template_name = "hold/entity_detail.html"

    def get_context_data(self, object, **kwargs):
        context = super().get_context_data(**kwargs)
        relevant_stakes = object.recursive_stakes
        context["entity_list"] = Entity.objects.order_by("name")
        context["stakes"] = Stake.objects.filter(
            pk__in=[s.id for s in relevant_stakes]
        ).order_by("-stake")
        context["create_entity_form"] = EntityForm()
        context["create_stake_form"] = StakeForm()
        return context


def _show_error_util(request, message):
    messages.add_message(
        request,
        messages.ERROR,
        message,
    )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("hold:home")))
