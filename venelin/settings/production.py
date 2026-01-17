import os
import warnings
from .common import *  # NOQA
from django.core.management.utils import get_random_secret_key

DEBUG = False

ADMINS = (
    ('Venelin Stoykov', 'v.k.stoykov@gmail.com'),
)
MANAGERS = ADMINS
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = [ADMINS[0][1]]

GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME")
GS_PROJECT_ID = os.getenv("GS_PROJECT_ID")
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}


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


# If runing during docker build we can skip the warnings about missing GOOGLE keys
if SECRET_KEY != 'management':
    if not SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:  # NOQA
        warnings.warn("GOOGLE_OAUTH2_KEY is not defined in environment! Login with Google disabled.")

    if not SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET:  # NOQA
        warnings.warn("GOOGLE_OAUTH2_SECRET is not defined in environment! Login with Google disabled.")
