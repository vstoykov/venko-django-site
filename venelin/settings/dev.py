import os

from .common import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'site.db'),
    },
}

CACHE_MIDDLEWARE_SECONDS = 10

ALLOWED_HOSTS = ['*']

DEFAULT_FROM_EMAIL = 'webmaster@venelin.sytes.net'
EMAIL_PORT = 1025

DISQUS_WEBSITE_SHORTNAME = 'venelin'

try:
    from .local import *
except ImportError:
    pass
