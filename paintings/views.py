from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from paintings.models import Announcement, HomePageImage, Piece


class HomeView(TemplateView):
    template_name = "paintings/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['announcement'] = Announcement.objects.filter(active=True).first()
        context['background_image'] = HomePageImage.objects.all().order_by('?').first()
        return context


class AnnouncementView(DetailView):
    model = Announcement
    template_name = "paintings/announcement.html"


class PieceView(DetailView):
    model = Piece
    template_name = "paintings/piece.html"

    def get_context_data(self, **kwargs):
        context = super(PieceView, self).get_context_data(**kwargs)
        order_field = Piece._meta.get_field_by_name('id')[0]
        context['next'] = self.object.get_next_by_field(order_field)
        context['previous'] = self.object.get_previous_by_field(order_field)
        return context


class WorksView(TemplateView):
    template_name = 'paintings/works.html'

    def get_context_data(self, **kwargs):
        context = super(WorksView, self).get_context_data(**kwargs)
        context['paintings'] = Piece.objects.all()
        return context
