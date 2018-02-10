from .common import *  # NOQA

DEBUG = False

ADMINS = (
    ('Venelin Stoykov', 'vkstoykov@gmail.com'),
)
MANAGERS = ADMINS

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

ALLOWED_HOSTS = [
    '*',
]

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'webmaster@venelin.sytes.net'


GOOGLE_ANALYTICS_CODE = 'UA-22285007-1'

try:
    from .local import *  # NOQA
except ImportError:
    pass
