"""woodypage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin


from paintings.views import HomeView, PaintingDetailView, PaintingsView, AnnouncementView, ContactView, ExhibitionsView, \
    ExhibitionDetailView, VideosView, VideoDetailView, WordsView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^announcement/(?P<pk>[-\w]+)$', AnnouncementView.as_view(), name='announcement'),
    url(r'^works/paintings$', PaintingsView.as_view(), name='paintings'),
    url(r'^works/paintings/(?P<pk>[-\w]+)$', PaintingDetailView.as_view(), name='painting'),
    url(r'^works/exhibitions$', ExhibitionsView.as_view(), name='exhibitions'),
    url(r'^works/exhibitions/(?P<pk>[-\w]+)$', ExhibitionDetailView.as_view(), name='exhibition'),
    url(r'^works/videos$', VideosView.as_view(), name='videos'),
    url(r'^works/videos/(?P<pk>[-\w]+)$', VideoDetailView.as_view(), name='video'),
    url(r'^words/(?P<pk>[-\w]+)$', WordsView.as_view(), name='words'),
    url(r'^words/$', WordsView.as_view(), name='featured_word'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^admin/', include(admin.site.urls)),
]

if not settings.DEPLOYED:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
