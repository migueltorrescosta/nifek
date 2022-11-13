from django.views import generic
from .models import Thesis


class ThesisList(generic.ListView):
    queryset = Thesis.objects.order_by('-created_on')
    template_name = 'index.html'


class ThesisDetail(generic.DetailView):
    model = Thesis
    template_name = 'thesis_detail.html'
