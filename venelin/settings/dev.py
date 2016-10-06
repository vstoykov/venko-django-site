from .common import *  # NOQA

import os


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'site.db'),
    },
}




CACHE_MIDDLEWARE_SECONDS = 10

ALLOWED_HOSTS = ['*']

DEFAULT_FROM_EMAIL = 'webmaster@venelin.sytes.net'
EMAIL_PORT = 1025

USE_DEBUG_TOOLABR = True

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
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES

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
        'debug_toolbar.panels.logging.LoggingPanel',
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
    MIDDLEWARE_CLASSES = (
        'venelin.middleware.SQLPrintingMiddleware',
    ) + MIDDLEWARE_CLASSES