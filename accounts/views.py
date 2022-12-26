import logging
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages

from accounts.models import User

logger = logging.getLogger(__name__)


class EditProfile(generic.DetailView):
    model = User
    template_name = "accounts/edit_profile.html"

    def get_object(self, queryset=None):
        print(self.request.user)
        print(User.objects.get(pk=self.request.user.pk))
        return User.objects.get(pk=self.request.user.pk)
