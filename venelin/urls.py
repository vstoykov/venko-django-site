from django.conf.urls import url, patterns, include
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from sitemap import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),

    (r'^blog/', include('blog.urls')),
    (r'^links/', include('links.urls')),
    (r'^gallery/', include('gallery.urls')),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^', include('pages.urls')),
)

if 'django_uwsgi' in settings.INSTALLED_APPS:
    urlpatterns = patterns('',
        (r'^admin/uwsgi/', include('django_uwsgi.urls')),
    ) + urlpatterns

# Static URLS is served by server. Django serves they only in DEBUG mode
if settings.DEBUG:
    urlpatterns = patterns('django.views.static',
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^(?P<path>favicon\.ico)$', 'serve', {'document_root': settings.STATIC_ROOT}),
    ) + staticfiles_urlpatterns() + urlpatterns
