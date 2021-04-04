# Django settings for doommaster project.
import re
import os
import posixpath

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'site.db'),
    },
}

DISQUS_WEBSITE_SHORTNAME = 'venelin'


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

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'venelin', 'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
STATIC_ROOT = os.path.join(BASE_DIR, 'wsgi', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'wsgi', 'media')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
STATIC_URL = '/static/'
MEDIA_URL = '/media/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qi!k%l+n@hs8l8%)t@j2bl6_jj_x2q-g^em=i!6m17(7x1^$9r'

# List of callables that know how to import templates from various sources.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'venelin', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'venelin.context_processors.google_analytics',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        }
    },
]


DISALLOWED_USER_AGENTS = (
    re.compile(r'^.*(ZmEu|[Ss]cann).*$'),
)

MIDDLEWARE = (
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'venelin.middleware.MinifyHTMLMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'venelin.middleware.XUACompatibleMiddleware',
)

ROOT_URLCONF = 'venelin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'venelin.wsgi.application'

INSTALLED_APPS = (
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

    'social_django',
    'django_extensions',
    'ckeditor',
    'imagekit',

    'venelin',
    'venelin.pages',
    'venelin.links',
    'venelin.blog',
    'venelin.gallery',
    'venelin.syntaxhighlighter',
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

INTERNAL_IPS = ('127.0.0.1',)

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google_openidconnect.GoogleOpenIdConnect',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_user',
)

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
        'contentsCss': posixpath.join(STATIC_URL, 'css/style.css'),
    },
}

WPADMIN = {
    'admin': {
        'menu': {
            'top': 'wpadmin.menu.menus.BasicTopMenu',
            'left': 'wpadmin.menu.menus.BasicLeftMenu',
        },
        'custom_style': posixpath.join(STATIC_URL, 'css/wpadmin-fix.css'),
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'stderr': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['stderr'],
            'propagate': False
        },
    },
}


SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

try:
    __import__('django_uwsgi')
except ImportError:
    pass
else:
    INSTALLED_APPS += ('django_uwsgi',)
