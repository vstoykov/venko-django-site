import os
import warnings
from .common import *  # NOQA
from django.core.management.utils import get_random_secret_key

DEBUG = False

ADMINS = (
    ('Venelin Stoykov', 'vkstoykov@gmail.com'),
)
MANAGERS = ADMINS
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = [ADMINS[0][1]]

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

if not SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:  # NOQA
    warnings.warn("GOOGLE_OAUTH2_KEY is not defined in environment! Login with Google disabled.")

if not SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET:  # NOQA
    warnings.warn("GOOGLE_OAUTH2_SECRET is not defined in environment! Login with Google disabled.")
