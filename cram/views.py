from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .enums import RevisionStatus
from .exceptions import NoNextCardException
from .forms import CardForm, UserCardScoreForm
from .models import Card, Collection, UserCardScore


def home(request):
    url = reverse("cram:collections")
    return redirect(url)


def star_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    if request.user not in collection.starred_by.all():
        collection.starred_by.add(request.user)
        collection.save()
    else:
        messages.info(request, "You have already starred this collection")
    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse("cram:collection_detail", kwargs={"pk": pk}),
        )
    )


def unstar_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    if request.user in collection.starred_by.all():
        collection.starred_by.remove(request.user)
        collection.save()
    else:
        messages.info(request, "This collection was already not starred by you")
    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse("cram:collection_detail", kwargs={"pk": pk}),
        )
    )


def review(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to review cards")
        return redirect("magiclink:login")

    try:
        next_user_card_score = UserCardScore.get_user_next_card_score(request.user)
    except NoNextCardException as e:
        messages.info(request, str(e))
        return redirect("cram:collections")

    number_of_cards_to_review = (
        UserCardScore.objects.filter(user=request.user)
        .filter(next_revision_timestamp__lte=timezone.now())
        .filter(card__collection__starred_by=request.user)
        .count()
    )
    number_of_cards_to_learn = (
        Card.objects.filter(collection__starred_by=request.user)
        .exclude(cram_scores__user=request.user)
        .count()
    )
    context = {
        "number_of_cards_to_review": number_of_cards_to_review,
        "number_of_cards_to_learn": number_of_cards_to_learn,
        "user_card_score": next_user_card_score,
    }
    return render(request, "cram/review.html", context=context)


class UserCardScoreDetailView(generic.UpdateView):

    model = UserCardScore

    def post(self, request, *args, **kwargs):
        revision = RevisionStatus(int(request.POST.get("last_revision")))

        user_card_score = self.get_object()
        user_card_score.process_revision(revision)
        return redirect("cram:review")


class CollectionListView(generic.ListView):
    model = Collection
    template_name = "cram/index.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if (
            self.request.user.is_authenticated
            and self.request.GET.get("show-all", None) is None
            and queryset.filter(owner=self.request.user).exists()
        ):
            queryset = queryset.filter(owner=self.request.user)
        queryset = queryset.annotate(count=Count("cram_cards"))
        return queryset


class CollectionDetail(generic.DetailView):
    model = Collection
    template_name = "cram/collection_detail.html"

    def get_context_data(self, object, **kwargs):
        context = super().get_context_data(**kwargs)
        context["starred"] = bool(self.request.user in object.starred_by.all())
        context["create_card_form"] = CardForm()
        return context

    def post(self, request, pk):
        # Creates a card and adds it to the collection

        if not request.user.is_authenticated:
            messages.add_message(
                request,
                messages.ERROR,
                "You cannot post a Thesis without logging in",
            )
            return HttpResponseRedirect(
                request.META.get(
                    "HTTP_REFERER",
                    reverse("cram:collection_detail", kwargs={"pk": pk}),
                )
            )

        collection = Collection.objects.get(pk=pk)

        if not request.user == collection.owner:
            messages.add_message(
                request,
                messages.ERROR,
                "You cannot Add a Card to a Collection you do not own",
            )
            return HttpResponseRedirect(
                request.META.get(
                    "HTTP_REFERER",
                    reverse("cram:collection_detail", kwargs={"pk": pk}),
                )
            )

        form = CardForm(data=request.POST)
        card = form.save(commit=False)
        card.collection = collection
        card.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Card {card.concept} created successfully",
        )
        return HttpResponseRedirect(
            request.META.get(
                "HTTP_REFERER",
                reverse("cram:collection_detail", kwargs={"pk": pk}),
            )
        )
