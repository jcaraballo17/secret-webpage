from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from paintings.models import Announcement, HomePageImage, Painting, Video, Exhibition, Word


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


class PaintingsView(ListView):
    model = Painting
    template_name = 'paintings/works/paintings.html'
    context_object_name = 'paintings'


class PaintingDetailView(DetailView):
    model = Painting
    template_name = "paintings/works/painting.html"

    def get_context_data(self, **kwargs):
        context = super(PaintingDetailView, self).get_context_data(**kwargs)
        order_field = Painting._meta.get_field('id')
        context['next'] = self.object.get_next_by_field(order_field)
        context['previous'] = self.object.get_previous_by_field(order_field)
        return context


class ExhibitionsView(ListView):
    model = Exhibition
    template_name = 'paintings/works/exhibitions.html'
    context_object_name = 'exhibitions'


class ExhibitionDetailView(DetailView):
    model = Exhibition
    template_name = "paintings/works/exhibition.html"


class VideosView(ListView):
    model = Video
    template_name = 'paintings/works/videos.html'
    context_object_name = 'videos'


class VideoDetailView(DetailView):
    model = Video
    template_name = "paintings/works/video.html"

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        order_field = Video._meta.get_field('id')
        context['next'] = self.object.get_next_by_field(order_field)
        context['previous'] = self.object.get_previous_by_field(order_field)
        return context


class WordsView(DetailView):
    model = Word
    template_name = 'paintings/words.html'

    def get_context_data(self, **kwargs):
        context = super(WordsView, self).get_context_data(**kwargs)
        context['sticky_words'] = Word.objects.filter(sticky=True)
        context['words_list'] = Word.objects.filter(sticky=False)
        return context

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super(WordsView, self).get_object(queryset)

        featured_queryset = Word.objects.filter(featured=True)
        return featured_queryset.get() if featured_queryset.exists() else None


class ContactView(TemplateView):
    template_name = "paintings/contact.html"
