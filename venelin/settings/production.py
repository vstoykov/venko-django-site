import os
import warnings
from .common import *  # NOQA
from django.core.management.utils import get_random_secret_key

DEBUG = False

ADMINS = (
    ('Venelin Stoykov', 'vkstoykov@gmail.com'),
)
MANAGERS = ADMINS

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

ALLOWED_HOSTS = [
    '*',
]

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'webmaster@stoykov.tk'


GOOGLE_ANALYTICS_CODE = 'UA-22285007-1'

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

try:
    from .local import *  # NOQA
except ImportError:
    pass

# Start with secure secret key no matter what. If not provided from environment
# can loose sessions on restart but other than that it's not a problem.
if not SECRET_KEY:
    warnings.warn("DJANGO_SECRET_KEY is not defined in environment! Generate random one.")
    SECRET_KEY = get_random_secret_key()
