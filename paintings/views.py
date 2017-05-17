from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from paintings.models import Announcement, HomePageBackground, Painting, Video, Exhibition, Word


class HomeView(TemplateView):
    template_name = 'paintings/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['active_announcement'] = Announcement.objects.filter(active=True).first()
        context['background_image'] = HomePageBackground.objects.all().order_by('?').first()
        return context


class AnnouncementView(DetailView):
    model = Announcement
    context_object_name = 'announcement'
    template_name = 'paintings/sections/announcement.html'


class PaintingsView(ListView):
    model = Painting
    template_name = 'paintings/sections/works/paintings_list.html'
    context_object_name = 'paintings'


class PaintingDetailView(DetailView):
    model = Painting
    context_object_name = 'painting'
    template_name = 'paintings/sections/works/painting_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PaintingDetailView, self).get_context_data(**kwargs)
        order_field = Painting._meta.get_field('id')
        context['next'] = self.object.get_next_by_field(order_field)
        context['previous'] = self.object.get_previous_by_field(order_field)
        return context


class VideosView(ListView):
    model = Video
    template_name = 'paintings/sections/works/videos_list.html'
    context_object_name = 'videos'


class VideoDetailView(DetailView):
    model = Video
    context_object_name = 'video'
    template_name = 'paintings/sections/works/video_detail.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        order_field = Video._meta.get_field('id')
        context['next'] = self.object.get_next_by_field(order_field)
        context['previous'] = self.object.get_previous_by_field(order_field)
        return context


class ExhibitionsView(DetailView):
    model = Exhibition
    context_object_name = 'exhibition'
    template_name = 'paintings/sections/works/exhibitions.html'

    def get_context_data(self, **kwargs):
        context = super(ExhibitionsView, self).get_context_data(**kwargs)
        context['exhibitions_list'] = Exhibition.objects.all()
        return context

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super(ExhibitionsView, self).get_object(queryset)
        return Exhibition.objects.first()


class WordsView(DetailView):
    model = Word
    context_object_name = 'word_entry'
    template_name = 'paintings/sections/words.html'

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
    template_name = 'paintings/sections/contact.html'
