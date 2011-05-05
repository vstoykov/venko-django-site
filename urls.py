from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from blog import urls as blog_urls

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/',  include(blog_urls)),
)

urlpatterns = urlpatterns + patterns('links.views',
    url(r'^links/$', 'links'),
)

urlpatterns = urlpatterns + patterns('gallery.views',
    url(r'^gallery/$', 'view_galleries', name='galleries'),
    url(r'^gallery/(?P<gallery>[\w\_\-]+)/$', 'view_galleries', name='gallery'),
)

urlpatterns = urlpatterns + patterns('pages.views',
    url(r'^home/$', 'home', name='home'),
)

# Redirect empty url to home page
urlpatterns = urlpatterns + patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': '/home/'}),
    url(r'^gallery_static/$', 'direct_to_template', {'template': 'gallery_static.html'}),
)

# Static URLS is served by server. Django serves they only in DEBUG mode
if settings.DEBUG:
    urlpatterns = urlpatterns + patterns('django.views.static',
        url(r'^favicon.ico', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'path':'favicon.png'}),
            
        url(r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )