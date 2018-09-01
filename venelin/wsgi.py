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
