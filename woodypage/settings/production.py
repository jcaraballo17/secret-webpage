__author__ = 'jcaraballo17'

from woodypage.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', data["host"]]

STATIC_ROOT = data["static_root"]
STATIC_URL = "/static/"

SITE_ROOT = "/opt/woodypage/"
SITE_URL = ""

MEDIA_ROOT = data["media_root"]
MEDIA_URL = "/media/"
