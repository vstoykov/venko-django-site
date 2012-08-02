from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from sitemap import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^blog/', include('blog.urls')),
    (r'^links/', include('links.urls')),
    (r'^gallery/', include('gallery.urls')),

    (r'^', include('pages.urls')),
)

# Create sitemap
urlpatterns = urlpatterns + patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)

# Static URLS is served by server. Django serves they only in DEBUG mode
if settings.DEBUG:
    urlpatterns = urlpatterns + patterns('django.views.static',
        url(r'^favicon.ico', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'path':'favicon.png'}),
            
        url(r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
