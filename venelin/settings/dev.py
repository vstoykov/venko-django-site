from .common import *  # NOQA

DEBUG = True

CACHE_MIDDLEWARE_SECONDS = 10

ALLOWED_HOSTS = ['*']

DEFAULT_FROM_EMAIL = 'webmaster@stoykov.tk'
EMAIL_PORT = 1025

INTERNAL_IPS = ('127.0.0.1',)

USE_DEBUG_TOOLABR = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'site.db'),
    },
}

SECRET_KEY = 'qi!k%l+n@hs8l8%)t@j2bl6_jj_x2q-g^em=i!6m17(7x1^$9r'

try:
    from .local import *  # NOQA
except ImportError:
    pass

try:
    __import__('debug_toolbar')
except ImportError:
    USE_DEBUG_TOOLABR = False


if USE_DEBUG_TOOLABR:
    INSTALLED_APPS += 'debug_toolbar',
    MIDDLEWARE = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE

    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    try:
        __import__('template_timings_panel')
    except ImportError:
        pass
    else:
        INSTALLED_APPS += 'template_timings_panel',
        DEBUG_TOOLBAR_PANELS.insert(
            8,
            'template_timings_panel.panels.TemplateTimings.TemplateTimings'
        )
else:
    MIDDLEWARE = (
        'venelin.middleware.SQLPrintingMiddleware',
    ) + MIDDLEWARE
