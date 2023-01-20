import logging

from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.db.utils import DataError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from .forms import ThesisForm
from .models import Property, Tag, Thesis

logger = logging.getLogger(__name__)


class ThesisList(ListView):
    template_name = "thes/index.html"

    def get_queryset(self):
        query_string = self.request.GET.get("q", None)
        if query_string is None:
            return Thesis.objects.order_by("-created_on")
        else:
            return Thesis.query(query_string=query_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_thesis_form"] = ThesisForm()
        context["tag_counts"] = (
            Tag.objects.filter(thesis__in=context["thesis_list"])
            .values("thesis", "property__text")
            .annotate(count=Count(["thesis", "property__text"]))
            .order_by("-count")
        )
        context["q"] = self.request.GET.get("q", None)
        return context

    def post(self, request):

        if not request.user.is_authenticated:
            messages.add_message(
                request,
                messages.ERROR,
                "You cannot post a Thesis without logging in",
            )
            return HttpResponseRedirect("/thes/")
        form = ThesisForm(data=request.POST)

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
        thesis.search_vector = SearchVector("content")
        thesis.save()
        return HttpResponseRedirect("/thes/")


class ThesisDetail(DetailView):
    model = Thesis
    template_name = "thes/thesis_detail.html"


class TagThesisView(SingleObjectMixin, View):
    """Records the current user's interest in an author."""

    model = Thesis

    def post(self, request, *args, **kwargs):
        try:
            thesis = Thesis.objects.get(pk=kwargs["pk"])
        except:
            return _show_error_util(
                request, "An attempt to add a tag to a non-existing Thesis was made"
            )

        if not request.user.is_authenticated:
            return _show_error_util(request, "You need to be logged in to Tag a Thesis")

        property_text = request.POST["property"]
        if property_text == "":
            return _show_error_util(request, "You can't submit an empty tag!")

        try:
            property, _ = Property.objects.get_or_create(
                text=property_text, defaults={"author": request.user}
            )
        except DataError:
            return _show_error_util(
                request,
                "For the time being we are preventing tags that are longer than 20 characters. Apologies for any inconvenience caused 😇",
            )
        tag_already_exists = Tag.objects.filter(
            property=property,
            thesis=thesis,
            tagger=request.user,
            deleted_on__isnull=False,
        ).exists()
        if tag_already_exists:
            return _show_error_util(
                request, f"You already tagged this Thesis with {property_text}"
            )

        try:
            Tag.objects.get_or_create(
                property=property, thesis=thesis, tagger=request.user
            )

        except DataError:
            return _show_error_util(request, "Internal Server Error :(")

        messages.add_message(
            request,
            messages.SUCCESS,
            f"Successfully applied the tag '{request.POST['property']}'",
        )
        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER", reverse("thes:home"))
        )


def _show_error_util(request, message):
    messages.add_message(
        request,
        messages.ERROR,
        message,
    )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("thes:home")))
