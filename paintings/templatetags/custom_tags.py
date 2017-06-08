import re
from django import template

register = template.Library()

common_words = ['a', 'the', 'is', 'this', 'in', 'on', 'all']


@register.filter('keywords')
def generate_keywords(instance):
    """
    :param instance: model instance to get the keywords from.
    :return: a string containing all the keywords for this instance.
    """

    instance_title = instance.__str__().lower()
    reduced_title = filter(lambda word: (word not in common_words and word != ''), re.split(r'\W+', instance_title))
    keywords = ', '.join(str(keyword) for keyword in reduced_title)
    return keywords
