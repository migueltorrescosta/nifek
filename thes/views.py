import logging
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from .models import Thesis
from .forms import ThesisForm

logger = logging.getLogger(__name__)


class ThesisList(generic.ListView):
    queryset = Thesis.objects.order_by("-created_on")
    template_name = "thes/index.html"

    def get_context_data(self, **kwargs):
        context = super(ThesisList, self).get_context_data(**kwargs)
        context["create_thesis_form"] = ThesisForm()
        # context["messages"] = self.get("messages", [])
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
                "Invalid Thesis",
            )
            return HttpResponseRedirect("/thes/")
        thesis = form.save(commit=False)
        thesis.author = request.user
        thesis.save()
        return HttpResponseRedirect("/thes/")


class ThesisDetail(generic.DetailView):
    model = Thesis
    template_name = "thes/thesis_detail.html"
