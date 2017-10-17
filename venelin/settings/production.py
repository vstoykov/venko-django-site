from .common import *

DEBUG = False

ADMINS = (
    ('Venelin Stoykov', 'vkstoykov@gmail.com'),
)
MANAGERS = ADMINS


TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
]


STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

ALLOWED_HOSTS = [
    '*',
]

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'webmaster@venelin.sytes.net'


GOOGLE_ANALYTICS_CODE = 'UA-22285007-1'

try:
    from .local import *
except ImportError:
    pass
