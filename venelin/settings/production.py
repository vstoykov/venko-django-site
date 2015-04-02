from .openshift import *

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('Venelin Stoykov', 'vkstoykov@gmail.com'),
)
MANAGERS = ADMINS

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

ALLOWED_HOSTS = [
    '*',
]

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'webmaster@venelin.sytes.net'


GOOGLE_ANALYTICS_CODE = 'UA-22285007-1'
