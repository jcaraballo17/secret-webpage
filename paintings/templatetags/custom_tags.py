from urlparse import parse_qs
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter('youthumbnail')
def youtube_thumbnail(url):
    """
    :param url: string containing youtube video url.
    :return: a string containing the youtube thumbnail image for the video.
    """
    qs = url.split('?')
    video_id = parse_qs(qs[1])['v'][0]

    return "https://i.ytimg.com/vi_webp/%s/mqdefault.webp" % video_id
