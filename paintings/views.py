from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from paintings.models import Announcement


class HomeView(TemplateView):
    template_name = "paintings/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['announcement'] = Announcement.objects.filter(active=True).first()
        return context


class PieceView(DetailView):
    template_name = "paintings/piece.html"

    def get_object(self, queryset=None):
        return None


class WorksView(ListView):
    template_name = 'paintings/works.html'

    def get_queryset(self):
        return []