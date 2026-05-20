"""
WSGI config for https://stoykov.tk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

ENV = os.getenv("DJANGO_ENV") or "dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "venelin.settings.%s" % ENV)

from django.core.wsgi import get_wsgi_application  # NOQA

application = get_wsgi_application()

from django.conf import settings  # NOQA

if getattr(settings, 'USE_DEBUG_TOOLABR', False):
    print("Debug toolbar is enabled")
    print("Internal IPs: ", ", ".join(settings.INTERNAL_IPS))

