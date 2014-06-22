# Django settings for doommaster project.
import re
import os
from django.conf import global_settings
import appenlight_client.client as e_client

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


DISQUS_WEBSITE_SHORTNAME = 'venelin'

APPENLIGHT = e_client.get_config() if os.getenv('APPENLIGHT_KEY') else {}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Sofia'
DATETIME_FORMAT = "j M Y, H:i"
DATE_FORMAT = 'j M Y'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'bg'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qi!k%l+n@hs8l8%)t@j2bl6_jj_x2q-g^em=i!6m17(7x1^$9r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'venelin.context_processors.google_analytics',
)

DISALLOWED_USER_AGENTS = (
    re.compile(r'^.*(ZmEu|[Ss]cann).*$'),
)

MIDDLEWARE_CLASSES = (
    'appenlight_client.django_middleware.AppenlightMiddleware',
    'venelin.middleware.SQLPrintingMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'venelin.middleware.MinifyHTMLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'venelin.middleware.XUACompatibleMiddleware',
)

ROOT_URLCONF = 'venelin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'venelin.wsgi.application'

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django_admin_bootstrapped.bootstrap3',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    'django.contrib.webdesign',

    'south',
    'ckeditor',
    'imagekit',

    'venelin',
    'venelin.pages',
    'venelin.links',
    'venelin.blog',
    'venelin.gallery',
    'venelin.syntaxhighlighter',
)

INTERNAL_IPS = ('127.0.0.1',)

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            {'name': 'styles', 'items': ['Styles', 'Format']},
            {'name': 'editing', 'groups': ['find', 'selection', 'spellchecker'], 'items': ['Scayt']},
            {'name': 'clipboard', 'groups': ['clipboard', 'undo'], 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'tools', 'items': ['Maximize']},
            {'name': 'document', 'groups': ['mode', 'document', 'doctools'], 'items': ['Source']},
            '',
            {'name': 'basicstyles', 'groups': ['basicstyles', 'cleanup'], 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph', 'groups': ['list', 'indent', 'blocks', 'align', 'bidi'], 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'SpecialChar']},
        ],
        'contentsCss': os.path.join(STATIC_URL, 'css/style.css'),
    },
}

CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 24 * 3600  # One day
CACHE_MIDDLEWARE_ALIAS = 'pages'

# On production LocMem must be changed with Memcached
# LocMem is fast but is not memory efficient
# (does not share cached item between threads)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default',
    },
    'pages': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'static',
        'OPTIONS': {'MAX_ENTRIES': 1000},
        'TIMEOUT': CACHE_MIDDLEWARE_SECONDS,
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'static',
        'OPTIONS': {'MAX_ENTRIES': 2000},
        'TIMEOUT': 7 * 24 * 3600,  # One week
    },
}


try:
    __import__('django_extensions')
except ImportError:
    pass
else:
    INSTALLED_APPS += ('django_extensions',)


try:
    __import__('uwsgi_admin')
except ImportError:
    pass
else:
    INSTALLED_APPS += ('uwsgi_admin',)

try:
    __import__('django_uwsgi')
except ImportError:
    pass
else:
    INSTALLED_APPS += ('django_uwsgi',)
