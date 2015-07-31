from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class HomeView(TemplateView):
    template_name = "paintings/index.html"


class PieceView(DetailView):
    template_name = "paintings/piece.html"

    def get_object(self, queryset=None):
        return None
