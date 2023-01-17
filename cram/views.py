from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .enums import RevisionStatus
from .forms import UserCardScoreForm
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

    if not Collection.objects.filter(starred_by=request.user).exists():
        messages.error(
            request,
            "You have no collections starred. Star a collection to start learning.",
        )
        return redirect("cram:collections")

    if not Card.objects.filter(collection__starred_by=request.user).exists():
        messages.error(
            request,
            "You have no starred collections with at least one card. Star a collection to start learning.",
        )
        return redirect("cram:collections")

    next_user_card_score = (
        UserCardScore.objects.filter(user=request.user)
        .filter(next_revision_timestamp__lte=timezone.now())
        .order_by("next_revision_timestamp")
        .first()
    )

    if next_user_card_score is None:
        new_card = (
            Card.objects.filter(collection__starred_by=request.user)
            .exclude(cram_scores__user=request.user)
            .first()
        )
        if new_card is None:
            next_card_timestamp = (
                UserCardScore.objects.filter(user=request.user)
                .order_by("next_revision_timestamp")
                .first()
            ).next_revision_timestamp
            timedelta = next_card_timestamp - timezone.now()
            hours = int(timedelta.total_seconds() / 3600)
            minutes = int(timedelta.total_seconds() / 60) % 60
            messages.info(
                request,
                f"You have no cards to review at the moment. Come back in roughly {hours}H{minutes}",
            )
            return redirect("cram:collections")
        else:
            next_user_card_score = UserCardScore.objects.create(
                card=new_card,
                user=request.user,
                last_revision=RevisionStatus.AGAIN,
                number_of_failed_revisions=0,
            )
            next_user_card_score.save()

    context = {
        "user_card_score": next_user_card_score,
        "user_card_score_form": UserCardScoreForm(instance=next_user_card_score),
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
        return queryset


class CollectionDetail(generic.DetailView):
    model = Collection
    template_name = "cram/collection_detail.html"

    def get_context_data(self, object, **kwargs):
        context = super(CollectionDetail, self).get_context_data(**kwargs)
        context["starred"] = bool(self.request.user in object.starred_by.all())
        print("=" * 50)
        print(self.request.user)
        print(object.starred_by.all())
        print(self.request.user in object.starred_by.all())
        print(bool(self.request.user in object.starred_by.all()))
        print(context["starred"])
        return context
