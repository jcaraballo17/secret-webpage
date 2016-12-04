from urlparse import parse_qs
from django import template

from paintings.models import Video

register = template.Library()


@register.filter('embed')
def youtube_embed(url):
    """
    :param url: string containing youtube video url.
    :return: a string containing the youtube video embed url.
    """
    video_id = Video.youtube_url_validation(url)
    return "https://www.youtube.com/embed/%s?rel=0" % video_id


@register.filter('youthumbnail')
def youtube_thumbnail(url):
    """
    :param url: string containing youtube video url.
    :return: a string containing the youtube thumbnail image for the video.
    """
    video_id = Video.youtube_url_validation(url)
    return "http://i.ytimg.com/vi/%s/hqdefault.jpg" % video_id
