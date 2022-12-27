from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Entity, Stake
from .forms import EntityForm


def home(request):
    if request.method == "GET":
        return home_get_request(request)
    elif request.method == "POST":
        return home_post_request(request)


def home_get_request(request):
    """Selects a random entity to view"""
    entity = Entity.objects.order_by("?").first()
    url = reverse("hold:entity_detail", kwargs={"pk": entity.pk})
    # Render the HTML template index.html with the data in the context variable
    return redirect(url)


def home_post_request(request):

    # We always remain in the same page regardless of this submission success
    return_page = HttpResponseRedirect(request.META.get("HTTP_REFERER", "/hold/"))

    if not request.user.is_authenticated:
        messages.add_message(
            request,
            messages.ERROR,
            "You cannot add an Entity without logging in",
        )
        return return_page
    form = EntityForm(data=request.POST)

    if not form.is_valid():
        messages.add_message(
            request,
            messages.ERROR,
            "The submitted Entity is invalid",
        )
        return return_page

    try:
        thesis = form.save(commit=False)
        thesis.submitted_by = request.user
        thesis.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully submitted entity {thesis.name} by {request.user.username}",
        )
    except:
        messages.add_message(
            request,
            messages.ERROR,
            f"Failed to create entity {thesis.name}",
        )
    return return_page


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
        context["create_entity_form"] = EntityForm()
        return context

    def post(self, request):

        if not request.user.is_authenticated:
            messages.add_message(
                request,
                messages.ERROR,
                "You cannot add an Entity without logging in",
            )
            return HttpResponseRedirect("/thes/")
        form = EntityForm(data=request.POST)

        if not form.is_valid():
            messages.add_message(
                request,
                messages.ERROR,
                "The submitted Thesis is invalid",
            )
            return HttpResponseRedirect("/thes/")

        thesis = form.save(commit=False)
        thesis.author = request.user
        thesis.save()
        return HttpResponseRedirect("/thes/")
