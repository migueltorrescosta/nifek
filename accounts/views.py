import logging

from django.views.generic import DetailView

from accounts.models import User

logger = logging.getLogger(__name__)


class EditProfile(DetailView):
    model = User
    template_name = "accounts/edit_profile.html"

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)
