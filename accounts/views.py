import logging
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages

from accounts.models import User

logger = logging.getLogger(__name__)


class EditProfile(generic.DetailView):
    model = User
    template_name = "user/edit_profile.html"

    def get_context_data(self, **kwargs):
        context = super(EditProfile, self).get_context_data(**kwargs)
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
                "The submitted Thesis is invalid",
            )
            return HttpResponseRedirect("/thes/")

        thesis = form.save(commit=False)
        thesis.author = request.user
        thesis.save()
        return HttpResponseRedirect("/thes/")
