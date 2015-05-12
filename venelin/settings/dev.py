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

MIDDLEWARE_CLASSES = (
    'venelin.middleware.SQLPrintingMiddleware',
) + MIDDLEWARE_CLASSES


CACHE_MIDDLEWARE_SECONDS = 10

ALLOWED_HOSTS = ['*']

DEFAULT_FROM_EMAIL = 'webmaster@venelin.sytes.net'
EMAIL_PORT = 1025

try:
    from .local import *
except ImportError:
    pass

try:
    __import__('debug_toolbar')
except ImportError:
    pass
else:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
