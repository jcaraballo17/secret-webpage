from urlparse import parse_qs
from django import template

register = template.Library()


@register.filter('embed')
def youtube_embed(url):
    """
    :param url: string containing youtube video url.
    :return: a string containing the youtube video embed url.
    """
    qs = url.split('?')
    video_id = parse_qs(qs[1])['v'][0]

    return "https://www.youtube.com/embed/%s?rel=0" % video_id


@register.filter('youthumbnail')
def youtube_thumbnail(url):
    """
    :param url: string containing youtube video url.
    :return: a string containing the youtube thumbnail image for the video.
    """
    qs = url.split('?')
    video_id = parse_qs(qs[1])['v'][0]

    return "http://i.ytimg.com/vi/%s/hqdefault.jpg" % video_id
