import os

ENV = os.getenv("DJANGO_ENV") or os.getenv("OPENSHIFT_APP_NAME") and "openshift" or "dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "venelin.settings.%s" % ENV)

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
