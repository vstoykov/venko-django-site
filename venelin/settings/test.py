"""
Test settings: same as dev (including optional local.py side effects on other
options) but always use local disk for uploaded files.

Developers who enable GCS in local.py would otherwise hit the network during
pytest; CI has no local.py and already used FileSystemStorage.
"""
from .dev import *  # noqa: F403

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
