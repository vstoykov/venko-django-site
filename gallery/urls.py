from django.conf.urls.defaults import *

urlpatterns = patterns('gallery.views',
    url(r'^$', 'galleries', name='galleries'),
    url(r'^(?P<slug>[\w\_\-]+)/$', 'gallery', name='gallery'),
)
