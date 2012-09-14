from django.conf.urls.defaults import *

urlpatterns = patterns('gallery.views',
    url(r'^$', 'view_galleries', name='galleries'),
    url(r'^(?P<gallery>[\w\_\-]+)/$', 'view_galleries', name='gallery'),
)
