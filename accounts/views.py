import logging
from django.views import generic

from accounts.models import User

logger = logging.getLogger(__name__)


class EditProfile(generic.DetailView):
    model = User
    template_name = "accounts/edit_profile.html"

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)
