from django.conf.urls import url, patterns, include
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .sitemap import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),

    (r'^blog/', include('blog.urls', namespace='blog')),
    (r'^links/', include('links.urls', namespace='links')),
    (r'^gallery/', include('gallery.urls', namespace='gallery')),
    (r'^highlighter/', include('syntaxhighlighter.urls')),
    (r'^search/', 'django.shortcuts.render', {'template_name': 'search.html'}),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots\.txt$', 'django.shortcuts.render', {'template_name': 'robots.txt', 'content_type': 'text/plain; charset=utf-8'}),
    (r'^(?P<path>favicon\.ico)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

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
    ) + staticfiles_urlpatterns() + urlpatterns
